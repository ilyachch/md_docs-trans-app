import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import mistune
import pydantic

from md_translate.document.parser import TypedParser

from .blocks import BaseBlock, NewlineBlock

logger = logging.getLogger(__name__)


class MarkdownDocument(pydantic.BaseModel):
    source: Optional[Path] = None

    blocks: List[BaseBlock] = pydantic.Field(default_factory=list)

    def render(self) -> str:
        return '\n\n'.join(map(str, self.blocks))

    @classmethod
    def from_file(
        cls,
        path: Union[str, Path],
        ignore_cache: bool = False,
    ) -> 'MarkdownDocument':
        target_file = cls.__get_file_path(path)
        if not ignore_cache:
            try:
                return cls.restore(target_file)
            except FileNotFoundError:
                logger.info('Cache file not found. Loading from source')
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

    def cache(self) -> None:
        if not self.source:
            return
        dump_file = self.__get_dump_file_path(self.source)
        dump_file.write_text(self._dump_data())

    def _dump_data(self) -> str:
        blocks_dump = [block.dump() for block in self.blocks]
        clean_data = {
            'source': str(self.source),
            'blocks': blocks_dump,
        }
        return json.dumps(clean_data)

    @classmethod
    def restore(cls, source: Path) -> 'MarkdownDocument':
        dump_file = cls.__get_dump_file_path(source)
        if not dump_file.exists():
            raise FileNotFoundError('Temp file not found: %s', str(dump_file))
        return cls(blocks=cls._load_data(dump_file.read_text()), source=source)

    @staticmethod
    def _load_data(cache_data: str) -> List[BaseBlock]:
        content = json.loads(cache_data)
        return [BaseBlock.restore(block_data) for block_data in content['blocks']]

    @staticmethod
    def __get_dump_file_path(source: Path) -> Path:
        return Path(source.parent / (source.name + '.tmp'))
