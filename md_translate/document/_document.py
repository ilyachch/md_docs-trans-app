import json
from pathlib import Path
from typing import TYPE_CHECKING, List

import mistune
import pydantic

from md_translate.document import blocks
from md_translate.document.renderers import BlocksRenderer

if TYPE_CHECKING:
    from md_translate.providers._base import TranslationProvider


class TempFileNotFoundError(FileNotFoundError):
    pass


class MarkdownDocument(pydantic.BaseModel):
    source: Path
    blocks_data: List[blocks.BaseBlock]

    def translate(self, translation_provider: 'TranslationProvider', from_lang: str, to_lang: str):
        with translation_provider as provider:
            for block in self.blocks_data:
                if isinstance(block, blocks.Translatable) and block.should_be_translated():
                    block.translated_text = provider.translate(
                        block.get_data_to_translate(), from_lang, to_lang
                    )
                self.__dump()
            self.__dump()
        self.__save(from_lang, to_lang)

    def __dump(self):
        dump_file = Path(self.source.parent / (self.source.name + '.tmp'))
        dump_file.write_text(self.json(indent=4))

    def __save(self, from_lang: str, to_lang: str) -> None:
        target_file = Path(self.source.parent / (self.source.name + f'.{from_lang}-{to_lang}.md'))
        target_file.write_text(self.__build())

    def __build(self) -> str:
        return '\n\n'.join(str(block) for block in self.blocks_data)

    @classmethod
    def from_file(cls, source: Path, *, force_new: bool = False) -> 'MarkdownDocument':
        if force_new:
            return cls.__from_file(source)
        else:
            try:
                return cls.__restore(source)
            except TempFileNotFoundError:
                cls.__from_file(source)

    @classmethod
    def __restore(cls, source: Path) -> 'MarkdownDocument':
        dump_file = Path(source.parent / (source.name + '.tmp'))
        if not dump_file.exists():
            raise TempFileNotFoundError(f'Temp file not found: %s', str(dump_file))
        content = json.loads(dump_file.read_text())
        return cls.parse_obj(content)

    @classmethod
    def __from_file(cls, source: Path) -> 'MarkdownDocument':
        text = source.read_text()
        markdown_parser = mistune.create_markdown(renderer=BlocksRenderer())
        return cls(source=source, blocks_data=[b for b in markdown_parser(text) if b])
