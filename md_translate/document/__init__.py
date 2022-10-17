import json
from pathlib import Path
from typing import List

import mistune
import pydantic

from md_translate.document import blocks
from md_translate.document.renderers import BlocksRenderer


class MarkdownDocument(pydantic.BaseModel):
    source: Path
    blocks_data: List[blocks.BaseBlock]

    def build(self) -> str:
        return '\n\n'.join(str(block) for block in self.blocks_data)

    def dump(self):
        dump_file = Path(self.source.parent / (self.source.name + '.tmp'))
        dump_file.write_text(self.json(indent=4))

    @classmethod
    def restore(cls, source: Path) -> 'MarkdownDocument':
        dump_file = Path(source.parent / (source.name + '.tmp'))
        content = json.loads(dump_file.read_text())
        return cls.parse_obj(content)
        # return cls(source=source, blocks_data=blocks_data)

    @classmethod
    def from_file(cls, source: Path):
        text = source.read_text()
        markdown_parser = mistune.create_markdown(renderer=BlocksRenderer())
        return cls(source=source, blocks_data=[b for b in markdown_parser(text) if b])


file_path = Path(
    '/home/ilyachch/Projects/OpenSource/django-rest-framework-rusdoc/.reference/README.md'
)
