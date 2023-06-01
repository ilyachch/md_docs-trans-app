import json
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

import mistune

from md_translate.document.blocks import BaseBlock, NewlineBlock
from md_translate.document.parser import TypedParser
from md_translate.translators import BaseTranslatorProtocol

if TYPE_CHECKING:
    from md_translate.settings import Settings

logger = logging.getLogger(__name__)


class MarkdownDocument:
    _TRANSLATED_MARK = '<!-- TRANSLATED by md-translate -->'
    _CLEARING_RULES = [
        (re.compile(r'\n{3,}'), '\n\n'),
        (re.compile(r'\n{2,}$'), '\n'),
        (re.compile(r'(?<=[\w.,]) {2,}(?=\w)'), ' '),
    ]

    def __init__(
        self,
        *,
        settings: 'Settings',
        source: Optional[Path] = None,
        blocks: Optional[list[BaseBlock]] = None,
    ) -> None:
        self._settings = settings
        self.source = source
        self.blocks = blocks or []

    def write(
        self,
    ) -> None:
        if not self.source:  # pragma: no cover
            raise ValueError('Only documents with source can be written')
        file_to_write = (
            self.source if not self._settings.new_file else self.__get_new_file_path(self.source)
        )
        file_to_write.write_text('\n'.join([self._TRANSLATED_MARK, self.render_translated()]))
        if not self._settings.save_temp_on_complete:
            temp_file = self.__get_dump_file_path(self.source)
            temp_file.unlink(missing_ok=True)

    def render(self) -> str:
        prerendered = '\n\n'.join(map(str, self.blocks)) + '\n'
        return self.__clear_rendered(prerendered)

    def render_translated(self) -> str:
        rendered_blocks = []
        for block in self.blocks:
            if not self._settings.drop_original:
                rendered_blocks.append(str(block))
                if block.translated_data:
                    rendered_blocks.append(block.translated_data)
            else:
                if block.translated_data:
                    rendered_blocks.append(block.translated_data)
                else:
                    rendered_blocks.append(str(block))
        prerendered = '\n\n'.join(rendered_blocks)
        return self.__clear_rendered(prerendered)

    def translate(self, translator: BaseTranslatorProtocol) -> None:
        blocks_to_translate = [block for block in self.blocks if block.should_be_translated]
        logger.info('Found %s blocks to translate', len(blocks_to_translate))
        for number, block in enumerate(blocks_to_translate, start=1):
            translated_data = translator.translate(text=str(block))
            block.translated_data = translated_data
            self.cache()
            logger.info('Translated block %s of %s', number, len(blocks_to_translate))
            logger.debug(f'Translated block: {block}')

    def should_be_translated(self) -> bool:
        if not self.source:
            return False
        if self._settings.overwrite:
            return True
        if self._settings.new_file:
            target_file = self.__get_new_file_path(self.source)
            if not target_file.exists():
                return True
            else:
                return self._TRANSLATED_MARK not in target_file.read_text()
        else:
            return self._TRANSLATED_MARK not in self.source.read_text()

    @classmethod
    def from_file(cls, path: Union[str, Path], settings: 'Settings') -> 'MarkdownDocument':
        target_file = cls.__get_file_path(path)
        if not settings.ignore_cache:
            try:
                return cls.restore(source=target_file, settings=settings)
            except FileNotFoundError:
                logger.info('Cache file not found. Loading from source')
        file_content = target_file.read_text()
        return cls(settings=settings, blocks=cls.__parse_blocks(file_content), source=target_file)

    @classmethod
    def from_string(cls, text: str, settings: 'Settings') -> 'MarkdownDocument':
        return cls(blocks=cls.__parse_blocks(text), settings=settings)

    def cache(self) -> None:
        if not self.source:
            return  # pragma: no cover
        dump_file = self.__get_dump_file_path(self.source)
        dump_file.write_text(self._dump_data())

    @classmethod
    def restore(cls, source: Path, settings: 'Settings') -> 'MarkdownDocument':
        dump_file = cls.__get_dump_file_path(source)
        if not dump_file.exists():
            raise FileNotFoundError('Temp file not found: %s', str(dump_file))
        return cls(blocks=cls._load_data(dump_file.read_text()), source=source, settings=settings)

    def _dump_data(self) -> str:
        blocks_dump = [block.dump() for block in self.blocks]
        clean_data = {
            'source': str(self.source),
            'blocks': blocks_dump,
        }
        return json.dumps(clean_data)

    def __clear_rendered(self, string: str) -> str:
        for pattern, replacement in self._CLEARING_RULES:
            string = pattern.sub(replacement, string)
        return string

    @staticmethod
    def _load_data(cache_data: str) -> list[BaseBlock]:
        content = json.loads(cache_data)
        return [BaseBlock.restore(block_data) for block_data in content['blocks']]

    @staticmethod
    def __get_file_path(path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            return Path(path)
        return path

    @staticmethod
    def __get_new_file_path(path: Path) -> Path:
        return path.with_name(f'{path.stem}_translated{path.suffix}')

    @staticmethod
    def __parse_blocks(text: str) -> list[BaseBlock]:
        markdown_parser = mistune.create_markdown(renderer=TypedParser())
        data = [b for b in markdown_parser(text) if b and not isinstance(b, NewlineBlock)]
        return data

    @staticmethod
    def __get_dump_file_path(source: Path) -> Path:
        return Path(source.parent / (source.name + '.tmp'))
