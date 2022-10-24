import abc
from typing import ClassVar, Generic, List, Optional, TypeVar

import pydantic


class AbstractBlock(abc.ABC, pydantic.BaseModel):
    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()


T = TypeVar('T', bound=AbstractBlock)


class Container(Generic[T], AbstractBlock):
    children: List[T]

    def __str__(self) -> str:
        return ''.join(map(str, self.children))


class NestedContainer(Generic[T], Container[T]):
    nested_children: List[T] = pydantic.Field(default_factory=list)

    def __str__(self) -> str:
        return ''.join(map(str, self.nested_children))


class Paragraph(Container[AbstractBlock]):
    def __str__(self):
        return ''.join(map(str, self.children))


class TextBlock(AbstractBlock):
    text: str

    def __str__(self) -> str:
        return self.text


class StrongTextBlock(Container[AbstractBlock], AbstractBlock):
    def __str__(self):
        return f'**{super().__str__()}**'


class EmphasisTextBlock(Container[AbstractBlock], AbstractBlock):
    def __str__(self):
        return f'*{super().__str__()}*'


class LinkBlock(Container[AbstractBlock], AbstractBlock):
    url: str
    title: Optional[str] = None

    def __str__(self) -> str:
        return f'[{self.title or super().__str__()}]({self.url})'


class ImageBlock(AbstractBlock):
    url: str
    alt: str = pydantic.Field(default=str)
    title: Optional[str] = None

    def __str__(self) -> str:
        title = f' "{self.title}"' if self.title else ''
        return f'![{self.alt}]({self.url}{title})'


class HeadingBlock(Container[AbstractBlock], AbstractBlock):
    level: int

    def __str__(self) -> str:
        return f'{"#" * self.level} {"".join(map(str, self.children))}'


class SeparatorBlock(AbstractBlock):
    def __str__(self) -> str:
        return '---'


class CodeSpanBlock(AbstractBlock):
    code: str

    def __str__(self) -> str:
        return f'`{self.code}`'


class CodeBlock(AbstractBlock):
    code: str
    language: Optional[str] = None

    def __str__(self) -> str:
        lang = self.language or ''
        return f'```{lang}\n{self.code}\n```'


class HtmlBlock(AbstractBlock):
    code: str

    def __str__(self) -> str:
        return self.code


class ListItemBlock(NestedContainer[AbstractBlock]):
    level: int

    def __str__(self) -> str:
        result = ''.join(map(str, self.children))
        if self.nested_children:
            nested_lines = ''.join(map(str, self.nested_children)).splitlines()
            processed_nested_lines = [' ' * 4 + line for line in nested_lines]
            result += '\n' + '\n'.join(processed_nested_lines)
        return result


class ListBlock(Container[ListItemBlock], AbstractBlock):
    ordered: bool = False
    level: int
    start: int = pydantic.Field(default=1)

    _MARKS: ClassVar[List[str]] = ['*', '-', '+']

    def __str__(self) -> str:
        rendered_children: List[str] = []
        if self.ordered:
            for i, child in enumerate(self.children, start=self.start):
                rendered_children.append(f'{i}. {child}')
        else:
            for child in self.children:
                # indent = ' ' * (child.level - 1) * 4
                mark = self._MARKS[(child.level - 1) % len(self._MARKS)]
                rendered_children.append(f'{mark} {child}')

        return '\n'.join(rendered_children)


class LineBreakBlock(AbstractBlock):
    def __str__(self) -> str:
        return '  \n'


class InlineHtmlBlock(HtmlBlock):
    def __str__(self):
        return f'`{self.code}`'


class NewlineBlock(AbstractBlock):
    def __str__(self):
        return '\n'


class BlockQuote(Container[AbstractBlock]):
    def __str__(self):
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
