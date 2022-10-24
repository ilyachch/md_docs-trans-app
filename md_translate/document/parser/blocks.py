from typing import Any, ClassVar, Dict, Generic, List, Optional, Type, TypeVar, cast

import pydantic


class BaseBlock(pydantic.BaseModel):
    def __str__(self) -> str:
        raise NotImplementedError()

    def dict(self, *args: Any, **kwargs: Any) -> dict:
        data = super().dict(*args, **kwargs)
        data['block_type'] = self.__class__.__name__
        return data

    @classmethod
    def restore(cls, values: Dict[str, Any]) -> 'BaseBlock':
        block_type_name = values.pop('block_type')
        if not block_type_name:
            raise ValueError('Unknown data. No block type found')
        block_type = blocks_registry.get(block_type_name)
        if not block_type:
            raise ValueError(f'Unknown block type: {block_type_name}')
        children = values.get('children')
        if children:
            parsed_children = []
            for child in children:
                parsed_children.append(BaseBlock.restore(child))
            values['children'] = parsed_children
        return block_type(**values)


blocks_registry: Dict[str, Type[BaseBlock]] = {}

T = TypeVar('T', bound=BaseBlock)


def register(cls: Type[T]) -> Type[T]:
    blocks_registry[cls.__name__] = cls
    return cls


class Container(Generic[T], BaseBlock):
    children: List[T]

    def __str__(self) -> str:
        return ''.join(map(str, self.children))


class NestedContainer(Generic[T], Container[T]):
    nested_children: List[T] = pydantic.Field(default_factory=list)

    def __str__(self) -> str:
        return ''.join(map(str, self.nested_children))


@register
class Paragraph(Container[BaseBlock]):
    def __str__(self) -> str:
        return ''.join(map(str, self.children))


@register
class TextBlock(BaseBlock):
    text: str

    def __str__(self) -> str:
        return self.text


@register
class StrongTextBlock(Container[BaseBlock]):
    def __str__(self) -> str:
        return f'**{super().__str__()}**'


@register
class EmphasisTextBlock(Container[BaseBlock]):
    def __str__(self) -> str:
        return f'*{super().__str__()}*'


@register
class LinkBlock(Container[BaseBlock]):
    url: str
    title: Optional[str] = None

    def __str__(self) -> str:
        return f'[{self.title or super().__str__()}]({self.url})'


@register
class ImageBlock(BaseBlock):
    url: str
    alt: str = pydantic.Field(default=str)
    title: Optional[str] = None

    def __str__(self) -> str:
        title = f' "{self.title}"' if self.title else ''
        return f'![{self.alt}]({self.url}{title})'


@register
class HeadingBlock(Container[BaseBlock]):
    level: int

    def __str__(self) -> str:
        return f'{"#" * self.level} {"".join(map(str, self.children))}'


@register
class SeparatorBlock(BaseBlock):
    def __str__(self) -> str:
        return '---'


@register
class CodeSpanBlock(BaseBlock):
    code: str

    def __str__(self) -> str:
        return f'`{self.code}`'


@register
class CodeBlock(BaseBlock):
    code: str
    language: Optional[str] = None

    @pydantic.validator('code', pre=True)
    def strip_code(cls, code: str) -> str:
        return code.strip()

    def __str__(self) -> str:
        lang = self.language or ''
        return f'```{lang}\n{self.code}\n```\n'


@register
class HtmlBlock(BaseBlock):
    code: str

    def __str__(self) -> str:
        return self.code


@register
class ListItemBlock(NestedContainer[BaseBlock]):
    level: int

    def __str__(self) -> str:
        result = ''.join(map(str, self.children))
        if self.nested_children:
            nested_lines = ''.join(map(str, self.nested_children)).splitlines()
            processed_nested_lines = [' ' * 4 + line for line in nested_lines]
            result += '\n' + '\n'.join(processed_nested_lines)
        return result


@register
class ListBlock(Container[ListItemBlock]):
    ordered: bool = False
    level: int
    start: Optional[int] = None

    _MARKS: ClassVar[List[str]] = ['*', '-', '+']

    def __str__(self) -> str:
        rendered_children: List[str] = []
        if self.ordered:
            self.start = cast(int, self.start)
            for i, child in enumerate(self.children, start=self.start):
                rendered_children.append(f'{i}. {child}')
        else:
            for child in self.children:
                # indent = ' ' * (child.level - 1) * 4
                mark = self._MARKS[(child.level - 1) % len(self._MARKS)]
                rendered_children.append(f'{mark} {child}')

        return '\n'.join(rendered_children)


@register
class LineBreakBlock(BaseBlock):
    def __str__(self) -> str:
        return '  \n'


@register
class InlineHtmlBlock(HtmlBlock):
    def __str__(self) -> str:
        return f'`{self.code}`'


@register
class NewlineBlock(BaseBlock):
    def __str__(self) -> str:
        return '\n'


@register
class BlockQuote(Container[BaseBlock]):
    def __str__(self) -> str:
        rendered_children = list(map(str, self.children))
        result = []
        for child in rendered_children:
            if child == '\n':
                result.append('>')
            elif '\n' in child:
                result.append('\n'.join(f'> {line}' for line in child.splitlines()))
            elif child.startswith('>'):
                result.append(f'>{child}')
            else:
                result.append(f'> {str(child)}')
        return '\n'.join(result)
