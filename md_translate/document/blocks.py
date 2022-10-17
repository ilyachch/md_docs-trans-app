from typing import Any, ClassVar, List, Optional, Type, Dict

import pydantic


class BlocksRegistry:
    def __init__(self):
        self.blocks_map = dict()

    def register(self, block: Type['BaseBlock']):
        self.blocks_map[block.__name__] = block
        return block

    def get_by_block_name(self, block_name: str) -> Type['BaseBlock']:
        return self.blocks_map[block_name]


block_registry = BlocksRegistry()


class BaseBlock(pydantic.BaseModel):
    IS_TRANSLATABLE: ClassVar[bool] = False

    @pydantic.root_validator(pre=True)
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(values, dict):
            children = values.get('children')
            if children:
                parsed_children = []
                for child in children:
                    if isinstance(child, dict):
                        block_type = child.pop('block_type')
                        block = block_registry.get_by_block_name(block_type)(**child)
                    else:
                        block = child
                    parsed_children.append(block)
                values['children'] = parsed_children
        return values

    def dict(self, *args, **kwargs) -> dict:
        data = super().dict(*args, **kwargs)
        data['block_type'] = self.__class__.__name__
        return data

    def __str__(self) -> str:
        raise NotImplementedError()

    def data_to_translate(self) -> Optional[str]:
        raise NotImplementedError()


class Final(pydantic.BaseModel):
    text: str

    def __str__(self) -> str:
        return self.text


@block_registry.register
class RawDataBlock(BaseBlock):
    name: str
    data: Any

    def __str__(self) -> str:
        return str(self.data)

    def __bool__(self):
        return bool(self.data)

    def data_to_translate(self) -> Optional[str]:
        return None


@block_registry.register
class TextBlock(Final, BaseBlock):
    IS_TRANSLATABLE = True

    strong: bool = False
    emphasis: bool = False

    @pydantic.validator('text', pre=True)
    def validate_text(cls, value):
        if isinstance(value, list):
            return ' '.join(map(str, value))
        return value

    def __str__(self) -> str:
        if self.strong:
            return f'**{self.text}**'
        if self.emphasis:
            return f'*{self.text}*'
        return self.text

    def data_to_translate(self) -> Optional[str]:
        return self.text


@block_registry.register
class LinkBlock(BaseBlock):
    IS_TRANSLATABLE = True

    link: str
    title: Optional[str] = None
    text: Optional[List[BaseBlock]] = None

    def __str__(self) -> str:
        return f'[{str(" ".join(map(str, self.text)) or self.title)}]({self.link})'

    def data_to_translate(self) -> Optional[str]:
        return self.title


@block_registry.register
class ImageBlock(BaseBlock):
    IS_TRANSLATABLE = True

    src: str
    alt: str = pydantic.Field(default=str)
    title: Optional[str] = None

    def __str__(self) -> str:
        return f'![{self.alt}]({self.src})'

    def data_to_translate(self) -> Optional[str]:
        return self.alt


@block_registry.register
class HeadingBlock(Final, BaseBlock):
    level: int
    text: str

    def __str__(self) -> str:
        return f'{"#" * self.level} {str(self.text)}'

    def data_to_translate(self) -> Optional[str]:
        return self.text


@block_registry.register
class SeparatorBlock(BaseBlock):
    def __str__(self) -> str:
        return '---'

    def data_to_translate(self) -> Optional[str]:
        return None


@block_registry.register
class CodeBlock(BaseBlock):
    code: str
    language: Optional[str] = None

    def __str__(self) -> str:
        lang = self.language or ''
        return f'```{lang}\n{self.code}\n```'

    def data_to_translate(self) -> Optional[str]:
        return None


@block_registry.register
class HtmlBlock(BaseBlock):
    code: str

    def __str__(self) -> str:
        return self.code

    def data_to_translate(self) -> Optional[str]:
        return None


@block_registry.register
class ListItemBlock(BaseBlock):
    children: List[Final]

    def __str__(self) -> str:
        return ''.join([str(child) for child in self.children])

    def data_to_translate(self) -> Optional[str]:
        return None


@block_registry.register
class ListBlock(BaseBlock):
    children: List['ListItemBlock']
    ordered: bool = False

    def __str__(self) -> str:
        return '\n'.join(
            [
                f'{f"{counter}." if self.ordered else "*"} {str(item)}'
                for counter, item in enumerate(self.children)
            ]
        )

    def data_to_translate(self) -> Optional[str]:
        return None
