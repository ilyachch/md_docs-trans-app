import json
from pathlib import Path
from typing import Any, List, Optional, Union

import mistune
import pydantic

from .blocks import BaseBlock, NewlineBlock
from .parser import TypedParser


class MarkdownDocument(pydantic.BaseModel):
    source: Optional[Path] = None

    blocks: List[BaseBlock]

    clear_cache: bool = False
    force_load: bool = False
    allow_empty: bool = False

    @pydantic.root_validator
    def validate_blocks(cls, values: Any) -> Any:
        if not values['blocks'] and not values['allow_empty']:
            raise ValueError('Document is empty')
        return values

    def render(self) -> str:
        return '\n\n'.join(map(str, self.blocks))

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> 'MarkdownDocument':
        target_file = cls.__get_file_path(path)
        file_content = target_file.read_text()
        return cls(blocks=cls.__parse_blocks(file_content), source=target_file)

    @staticmethod
    def __get_file_path(path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            return Path(path)
        return path

    @classmethod
    def from_string(cls, text: str) -> 'MarkdownDocument':
        return cls(
            blocks=cls.__parse_blocks(text),
        )

    @staticmethod
    def __parse_blocks(text: str) -> List[BaseBlock]:
        markdown_parser = mistune.create_markdown(renderer=TypedParser())
        data = [b for b in markdown_parser(text) if b and not isinstance(b, NewlineBlock)]
        return data

    def dump(self) -> str:
        blocks_dump = [block.dump() for block in self.blocks]
        clean_data = {
            'source': str(self.source),
            'blocks': blocks_dump,
        }
        return json.dumps(clean_data)

    def cache(self) -> None:
        dump_file = self.__get_dump_file_path()
        if self.clear_cache:
            dump_file.write_text(self.dump())
        elif dump_file.exists():
            raise RuntimeError('Temp file already exists: %s', str(dump_file))

    def load(self, cache_data: str) -> None:
        content = json.loads(cache_data)
        self.blocks = [BaseBlock.restore(block_data) for block_data in content['blocks']]

    def restore(self) -> None:
        dump_file = self.__get_dump_file_path()
        if self.force_load:
            if not dump_file.exists():
                raise ValueError('Temp file not found: %s', str(dump_file))
            self.load(dump_file.read_text())

    def __get_dump_file_path(self) -> Path:
        if self.source:
            return Path(self.source.parent / (self.source.name + '.tmp'))
        raise ValueError('Source is not defined')
