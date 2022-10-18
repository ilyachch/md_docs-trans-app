import json
from pathlib import Path
from typing import TYPE_CHECKING, List, cast

import click
import mistune
import pydantic

from md_translate.document import _blocks as blocks
from md_translate.document._renderers import BlocksRenderer

if TYPE_CHECKING:
    from md_translate.providers._base import TranslationProvider


class TempFileNotFoundError(FileNotFoundError):
    pass


class MarkdownDocument(pydantic.BaseModel):
    source: Path
    blocks_data: List[blocks.BaseBlock]

    def translate(
        self,
        translation_provider: 'TranslationProvider',
        from_lang: str,
        to_lang: str,
        new_file: bool,
    ) -> None:
        with translation_provider as provider:
            for counter, block in enumerate(self.blocks_data, start=1):
                # if hasattr(block, 'children')
                if block.IS_TRANSLATABLE and block.should_be_translated():
                    block.translated_text = provider.translate(
                        from_language=from_lang,
                        to_language=to_lang,
                        text=block.get_data_to_translate(),
                    )
                    click.echo(f'Translated: {counter} of {len(self.blocks_data)}')
                self.__dump()
            self.__dump()
        self.__save(from_lang, to_lang, new_file)

    def __get_nested_translatable(self, block: blocks.BaseBlock):
        pass

    def __dump(self):
        dump_file = Path(self.source.parent / (self.source.name + '.tmp'))
        dump_file.write_text(self.json(indent=4))

    def __save(self, from_lang: str, to_lang: str, new_file: bool) -> None:
        if new_file:
            target_file = Path(
                self.source.parent / (self.source.name + f'.{from_lang}-{to_lang}.md')
            )
        else:
            target_file = self.source
        target_file.write_text(self._build())

    def _build(self) -> str:
        result = ''
        for block in self.blocks_data:
            result += str(block)
            if block.IS_TRANSLATABLE:
                block = cast(blocks.Translatable, block)
                if block.translated_text:
                    result += f'\n\n{block.translated_text}'
            result += '\n'
        return result

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
        return cls(
            source=content['source'],
            blocks_data=[blocks.BaseBlock(**block_data) for block_data in content['blocks_data']],
        )

    @classmethod
    def __from_file(cls, source: Path) -> 'MarkdownDocument':
        text = source.read_text()
        markdown_parser = mistune.create_markdown(renderer=BlocksRenderer())
        return cls(source=source, blocks_data=[b for b in markdown_parser(text) if b])
