from typing import Any, ClassVar, Generic, Optional, Type, TypeVar, cast

import pydantic


class BaseBlock(pydantic.BaseModel):
    translated_data: Optional[str] = None

    TRANSLATABLE: ClassVar[bool] = True

    @property
    def should_be_translated(self) -> bool:
        return self.TRANSLATABLE and self.translated_data is None

    def __str__(self) -> str:
        raise NotImplementedError(self.__class__.__name__)

    def dump(self) -> dict:
        data = self.dict(exclude_unset=True)
        data['block_type'] = self.__class__.__name__
        return data

    @classmethod
    def restore(cls, values: dict[str, Any]) -> 'BaseBlock':
        block_type_name = values.pop('block_type')
        if not block_type_name:
            raise ValueError('Unknown data. No block type found')  # pragma: no cover
        block_type = blocks_registry.get(block_type_name)
        if not block_type:
            raise ValueError(f'Unknown block type: {block_type_name}')  # pragma: no cover
        children = values.get('children')
        if children:
            parsed_children = []
            for child in children:
                parsed_children.append(BaseBlock.restore(child))
            values['children'] = parsed_children
        return block_type(**values)


T = TypeVar('T', bound=BaseBlock)


class BlocksRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, Type[BaseBlock]] = {}

    def get(self, block_type_name: str) -> Optional[Type[BaseBlock]]:
        return self._registry.get(block_type_name)

    def register(self, block_type: Type[T]) -> Type[T]:
        self._registry[block_type.__name__] = block_type
        return block_type


blocks_registry = BlocksRegistry()


class Container(Generic[T], BaseBlock):
    children: list[T]

    def __str__(self) -> str:
        return ''.join(map(str, self.children))

    def dump(self) -> dict:
        data = super().dump()
        data['children'] = [child.dump() for child in self.children]
        return data


class NestedContainer(Generic[T], Container[T]):
    nested_children: list[T] = pydantic.Field(default_factory=list)

    def __str__(self) -> str:  # pragma: no cover
        return ''.join(map(str, self.nested_children))


@blocks_registry.register
class Paragraph(Container[BaseBlock]):
    def __str__(self) -> str:
        return ''.join(map(str, self.children))


@blocks_registry.register
class TextBlock(BaseBlock):
    text: str

    def __str__(self) -> str:
        return self.text


@blocks_registry.register
class StrongTextBlock(Container[BaseBlock]):
    def __str__(self) -> str:
        return f'**{super().__str__()}**'


@blocks_registry.register
class EmphasisTextBlock(Container[BaseBlock]):
    def __str__(self) -> str:
        return f'_{super().__str__()}_'


@blocks_registry.register
class LinkBlock(Container[BaseBlock]):
    url: str
    title: Optional[str] = None

    def __str__(self) -> str:
        title = f' "{self.title}"' if self.title else ''
        return f'[{super().__str__()}]({self.url}{title})'


@blocks_registry.register
class ImageBlock(BaseBlock):
    url: str
    alt: str = pydantic.Field(default=str)
    title: Optional[str] = None

    def __str__(self) -> str:
        title = f' "{self.title}"' if self.title else ''
        return f'![{self.alt}]({self.url}{title})'


@blocks_registry.register
class HeadingBlock(Container[BaseBlock]):
    level: int

    def __str__(self) -> str:
        return f'{"#" * self.level} {"".join(map(str, self.children))}'


@blocks_registry.register
class SeparatorBlock(BaseBlock):
    TRANSLATABLE = False

    def __str__(self) -> str:
        return '---'


@blocks_registry.register
class CodeSpanBlock(BaseBlock):
    code: str

    def __str__(self) -> str:
        if '`' in self.code:
            return f'``{self.code}``'
        else:
            return f'`{self.code}`'


@blocks_registry.register
class CodeBlock(BaseBlock):
    TRANSLATABLE = False
    code: str
    language: Optional[str] = None

    @pydantic.validator('code', pre=True)
    def strip_code(cls, code: str) -> str:
        return code.strip()

    def __str__(self) -> str:
        lang = self.language or ''
        return f'```{lang}\n{self.code}\n```'


@blocks_registry.register
class HtmlBlock(BaseBlock):
    TRANSLATABLE = False
    code: str

    def __str__(self) -> str:
        return self.code


@blocks_registry.register
class ListItemBlock(NestedContainer[BaseBlock]):
    level: int

    def __str__(self) -> str:
        result = ''.join(map(str, self.children))
        if self.nested_children:
            nested_lines = ''.join(map(str, self.nested_children)).splitlines()
            processed_nested_lines = [' ' * 4 + line for line in nested_lines]
            result += '\n' + '\n'.join(processed_nested_lines)
        return result


@blocks_registry.register
class ListBlock(Container[ListItemBlock]):
    ordered: bool = False
    level: int
    start: Optional[int] = None

    _MARKS: ClassVar[list[str]] = ['*', '-', '+']

    def __str__(self) -> str:
        rendered_children: list[str] = []
        if self.ordered:
            self.start = cast(int, self.start)
            for i, child in enumerate(self.children, start=self.start):
                rendered_children.append(f'{i}. {child}')
        else:
            for child in self.children:
                mark = self._MARKS[(child.level - 1) % len(self._MARKS)]
                rendered_children.append(f'{mark} {child}')

        return '\n'.join(rendered_children) + '\n'


@blocks_registry.register
class LineBreakBlock(BaseBlock):
    def __str__(self) -> str:
        return '  \n'


@blocks_registry.register
class InlineHtmlBlock(HtmlBlock):
    def __str__(self) -> str:
        return f'{self.code}'


@blocks_registry.register
class NewlineBlock(BaseBlock):
    def __str__(self) -> str:
        return '\n'


@blocks_registry.register
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
