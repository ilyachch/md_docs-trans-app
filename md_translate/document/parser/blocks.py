import abc
from typing import List, Optional, Generic, TypeVar

import pydantic


class AbstractBlock(abc.ABC, pydantic.BaseModel):
    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()


T = TypeVar('T', bound=AbstractBlock)


class Container(Generic[T], AbstractBlock):
    children: List[T]

    def __str__(self) -> str:
        return '\n'.join(map(str, self.children))


class Paragraph(Container[AbstractBlock]):
    pass


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
        return f'![{self.alt}]({self.url} "{self.title or ""}")'


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


class ListItemBlock(Container[AbstractBlock]):
    level: int

    def __str__(self) -> str:
        indent = ' ' * (self.level - 1) * 4
        return f'{indent} {super().__str__()}'


class ListBlock(Container[ListItemBlock], AbstractBlock):
    ordered: bool = False
    level: int
    start: int = 1

    def __str__(self) -> str:
        rendered_children: List[str] = []
        if self.ordered:
            for i, child in enumerate(self.children, start=self.start):
                rendered_children.append(f'{self.start + i}. {child}')

        return '\n'.join(
            [
                f'{f"{counter}." if self.ordered else "*"} {str(item)}'
                for counter, item in enumerate(self.children)
            ]
        )


class LineBreakBlock(AbstractBlock):
    def __str__(self) -> str:
        return '  \n'


class InlineHtmlBlock(HtmlBlock):
    def __str__(self):
        return f'`{self.code}`'


class NewlineBlock(AbstractBlock):
    def __str__(self):
        return '\n'


class BlockQuote(Container[AbstractBlock], AbstractBlock):
    def __str__(self):
        return '> ' + super().__str__().replace('\n', '\n> ')
