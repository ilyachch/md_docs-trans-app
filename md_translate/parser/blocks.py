import abc
from typing import Any, List, Optional


class BaseBlock(abc.ABC):
    IS_TRANSLATABLE: bool = False

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def data_to_translate(self) -> Optional[str]:
        raise NotImplementedError()


class RawDataBlock(BaseBlock):
    def __init__(self, name: str, data: Any) -> None:
        self.name = name
        self.data = data

    def __str__(self) -> str:
        return str(self.data)

    def __bool__(self):
        return bool(self.data)

    def data_to_translate(self) -> Optional[str]:
        return None


class TextBlock(BaseBlock):
    IS_TRANSLATABLE = True

    def __init__(self, text: str, strong: bool = False, emphasis: bool = False) -> None:
        if isinstance(text, list) and all(isinstance(t, TextBlock) for t in text):
            text = ''.join(str(t) for t in text)
        self.strong = strong
        self.text = text
        self.emphasis = emphasis

    def __str__(self) -> str:
        if self.strong:
            return f'**{self.text}**'
        if self.emphasis:
            return f'*{self.text}*'
        return self.text

    def data_to_translate(self) -> str:
        return self.text


class LinkBlock(BaseBlock):
    IS_TRANSLATABLE = True

    def __init__(self, link: str, title: Optional[str] = None, text: Optional[str] = None) -> None:
        self.link = link
        self.title = title
        self.text = text

    def __str__(self) -> str:
        return f'[{str(self.text or self.title)}]({self.link})'

    def data_to_translate(self) -> Optional[str]:
        return self.title


class ImageBlock(BaseBlock):
    IS_TRANSLATABLE = True

    def __init__(self, src: str, alt: str = '', title: Optional[str] = None) -> None:
        self.src = src
        self.alt = alt
        self.title = title

    def __str__(self) -> str:
        return f'![{self.alt}]({self.src})'

    def data_to_translate(self) -> Optional[str]:
        return self.alt


class CodeSpanBlock(BaseBlock):
    IS_TRANSLATABLE = True

    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return f'`{self.text}`'

    def data_to_translate(self) -> Optional[str]:
        return self.text


class LineBreakBlock(BaseBlock):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return '\n'

    def data_to_translate(self) -> Optional[str]:
        return None


class InlineHtmlBlock(BaseBlock):
    def __init__(self, html: str) -> None:
        self.html = html

    def __str__(self) -> str:
        return self.html

    def data_to_translate(self) -> Optional[str]:
        return None


class HeadingBlock(BaseBlock):
    def __init__(self, level: int, children: List[BaseBlock]) -> None:
        self.level = level
        self.children = children

    def __str__(self) -> str:
        return f'{"#" * self.level} {" ".join([str(child) for child in self.children])}'

    def data_to_translate(self) -> Optional[str]:
        return None


class SeparatorBlock(BaseBlock):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return '---'

    def data_to_translate(self) -> Optional[str]:
        return None


class CodeBlock(BaseBlock):
    def __init__(self, code: str, language: Optional[str] = None) -> None:
        self.code = code
        self.language = language

    def __str__(self) -> str:
        lang = self.language or ''
        return f'```{lang}\n{self.code}\n```'

    def data_to_translate(self) -> Optional[str]:
        return None


class HtmlBlock(BaseBlock):
    def __init__(self, html: str) -> None:
        self.html = html

    def __str__(self) -> str:
        return self.html

    def data_to_translate(self) -> Optional[str]:
        return None


class ListBlock(BaseBlock):
    def __init__(self, items: List[BaseBlock], ordered: bool) -> None:
        self.items = items
        self.ordered = ordered

    def __str__(self) -> str:
        return '\n'.join(
            [
                f'{f"{counter}." if self.ordered else "*"} {" ".join([str(child) for child in item])}'
                for counter, item in enumerate(self.items)
            ]
        )

    def data_to_translate(self) -> Optional[str]:
        return None


class ListItemBlock(BaseBlock):
    def __init__(self, children: List[BaseBlock]) -> None:
        self.children = children

    def __str__(self) -> str:
        return ' '.join([str(child) for child in self.children])

    def data_to_translate(self) -> Optional[str]:
        return None
