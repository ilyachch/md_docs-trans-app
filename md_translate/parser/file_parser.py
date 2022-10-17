from pathlib import Path
from typing import List

import mistune

from md_translate.parser import blocks
from md_translate.parser.renderers import BlocksRenderer


class MarkdownDocument:
    def __init__(self, blocks_: List[blocks.BaseBlock]) -> None:
        self._blocks = blocks_

    @classmethod
    def from_file(cls, file_path: Path):
        text = file_path.read_text()
        markdown_parser = mistune.create_markdown(renderer=BlocksRenderer())
        return cls([b for b in markdown_parser(text) if b])


file_path = Path(
    '/home/ilyachch/Projects/OpenSource/django-rest-framework-rusdoc/.reference/README.md'
)
