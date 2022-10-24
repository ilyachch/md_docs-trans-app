from typing import Any, ClassVar, Generic, List, Optional, TypeVar

import pydantic


class BaseBlock(pydantic.BaseModel):
    IS_TRANSLATABLE: ClassVar[bool] = False

    @pydantic.root_validator(pre=True)
    def check(cls, values: Any) -> Any:
        if isinstance(values, dict):
            children = values.get('children')
            if children:
                parsed_children = []
                for child in children:
                    if isinstance(child, dict) and 'block_type' in child:
                        block_type = child.pop('block_type')
                        if block_type not in globals():
                            raise ValueError('Unknown Block Type: %s', block_type)
                        block = globals()[block_type](**child)
                    else:
                        block = child
                    parsed_children.append(block)
                values['children'] = parsed_children
        return values

    def dict(self, *args, **kwargs) -> dict:
        data = super().dict(*args, **kwargs)
        data['block_type'] = self.__class__.__name__
        return data

    def should_be_translated(self) -> bool:
        return False

    def __str__(self) -> str:
        raise NotImplementedError()


T = TypeVar('T', bound=BaseBlock)


class Container(Generic[T], BaseBlock):
    children: List[T]

    def __str__(self) -> str:
        return '\n'.join(str(child) for child in self.children)


class Translatable(BaseBlock):
    text: str
    translated_text: Optional[str] = None

    def __str__(self) -> str:
        return self.text

    def get_translated(self) -> Optional[str]:
        return self.translated_text if self.translated_text else None

    def should_be_translated(self) -> bool:
        return self.translated_text is None

    def get_data_to_translate(self):
        raise NotImplementedError()


class RawDataBlock(BaseBlock):
    name: str
    data: Any

    def __str__(self) -> str:
        return str(self.data)

    def __bool__(self):
        return bool(self.data)


class TextBlock(Translatable):
    IS_TRANSLATABLE = True

    @pydantic.validator('text', pre=True)
    def validate_text(cls, value):
        if isinstance(value, list):
            return ''.join(map(str, value))
        return value

    def get_data_to_translate(self):
        return self.text


class StrongTextBlock(TextBlock):
    def __str__(self):
        return f'**{self.text}**'


class EmphasisTextBlock(TextBlock):
    def __str__(self):
        return f'*{self.text}*'


class LinkBlock(BaseBlock):
    IS_TRANSLATABLE = True

    link: str
    title: Optional[str] = None
    text: Optional[List[BaseBlock]] = None

    def __str__(self) -> str:
        label = ''
        if self.text:
            label = ''.join(map(str, self.text))
        elif self.title:
            label = self.title
        return f'[{label}]({self.link})'


class ImageBlock(BaseBlock):
    IS_TRANSLATABLE = True

    src: str
    alt: str = pydantic.Field(default=str)
    title: Optional[str] = None

    def __str__(self) -> str:
        return f'![{self.alt}]({self.src})'


class HeadingBlock(Translatable, BaseBlock):
    level: int
    text: str

    def __str__(self) -> str:
        return f'{"#" * self.level} {str(self.text)}'

    def get_data_to_translate(self):
        return self.text


class SeparatorBlock(BaseBlock):
    def __str__(self) -> str:
        return '---'


class CodeBlock(BaseBlock):
    code: str
    language: Optional[str] = None

    def __str__(self) -> str:
        lang = self.language or ''
        return f'```{lang}\n{self.code}\n```'


class HtmlBlock(BaseBlock):
    code: str

    def __str__(self) -> str:
        return self.code


class ListItemBlock(Container[Translatable]):
    def __str__(self) -> str:
        return ''.join([str(child) for child in self.children])


class ListBlock(Container[ListItemBlock], BaseBlock):
    ordered: bool = False

    def __str__(self) -> str:
        return '\n'.join(
            [
                f'{f"{counter}." if self.ordered else "*"} {str(item)}'
                for counter, item in enumerate(self.children)
            ]
        )
