import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Union

import mistune
import pydantic

from md_translate.document.parser import TypedParser

from .blocks import BaseBlock, NewlineBlock

if TYPE_CHECKING:
    from md_translate.translators._base import TranslationProvider

logger = logging.getLogger(__name__)


class MarkdownDocument(pydantic.BaseModel):
    source: Optional[Path] = None

    blocks: List[BaseBlock] = pydantic.Field(default_factory=list)

    def write(
        self,
        *,
        new_file: bool = False,
        translated: bool = True,
        save_temp_on_complete: bool = False,
    ) -> None:
        if not self.source:  # pragma: no cover
            raise ValueError('Only documents with source can be written')
        file_to_write = self.source if not new_file else self.__get_new_file_path(self.source)
        if translated:
            file_to_write.write_text(self.render_translated())
            if not save_temp_on_complete:
                temp_file = self.__get_dump_file_path(self.source)
                temp_file.unlink(missing_ok=True)
        else:
            file_to_write.write_text(self.render())

    def render(self) -> str:
        return '\n\n'.join(map(str, self.blocks))

    def render_translated(self) -> str:
        rendered_blocks = []
        for block in self.blocks:
            rendered_blocks.append(str(block))
            if block.translated_data:
                rendered_blocks.append(block.translated_data)
        return '\n\n'.join(rendered_blocks)

    def translate(self, translator: 'TranslationProvider', from_lang: str, to_lang: str) -> None:
        blocks_to_translate = [block for block in self.blocks if block.should_be_translated]
        logger.info('Found %s blocks to translate', len(blocks_to_translate))
        for number, block in enumerate(blocks_to_translate, start=1):
            translated_data = translator.translate(
                from_language=from_lang, to_language=to_lang, text=str(block)
            )
            block.translated_data = translated_data
            self.cache()
            logger.info('Translated block %s of %s', number, len(blocks_to_translate))
            logger.debug(f'Translated block: {block}')

    def should_be_translated(self, new_file: bool = False, overwrite: bool = False) -> bool:
        if overwrite:
            return True
        if not self.source:
            return False
        target_file = self.source if not new_file else self.__get_new_file_path(self.source)
        return not target_file.exists()

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

    @classmethod
    def from_string(cls, text: str) -> 'MarkdownDocument':
        return cls(
            blocks=cls.__parse_blocks(text),
        )

    def cache(self) -> None:
        if not self.source:
            return  # pragma: no cover
        dump_file = self.__get_dump_file_path(self.source)
        dump_file.write_text(self._dump_data())

    @classmethod
    def restore(cls, source: Path) -> 'MarkdownDocument':
        dump_file = cls.__get_dump_file_path(source)
        if not dump_file.exists():
            raise FileNotFoundError('Temp file not found: %s', str(dump_file))
        return cls(blocks=cls._load_data(dump_file.read_text()), source=source)

    def _dump_data(self) -> str:
        blocks_dump = [block.dump() for block in self.blocks]
        clean_data = {
            'source': str(self.source),
            'blocks': blocks_dump,
        }
        return json.dumps(clean_data)

    @staticmethod
    def _load_data(cache_data: str) -> List[BaseBlock]:
        content = json.loads(cache_data)
        return [BaseBlock.restore(block_data) for block_data in content['blocks']]

    @staticmethod
    def __get_file_path(path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            return Path(path)
        return path

    def __get_new_file_path(self, path: Path) -> Path:
        return path.with_name(f'{path.stem}_translated{path.suffix}')

    @staticmethod
    def __parse_blocks(text: str) -> List[BaseBlock]:
        markdown_parser = mistune.create_markdown(renderer=TypedParser())
        data = [b for b in markdown_parser(text) if b and not isinstance(b, NewlineBlock)]
        return data

    @staticmethod
    def __get_dump_file_path(source: Path) -> Path:
        return Path(source.parent / (source.name + '.tmp'))
