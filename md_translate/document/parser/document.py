from pathlib import Path
from typing import List, Optional

import mistune
import pydantic

from .blocks import AbstractBlock, NewlineBlock
from .parser import TypedParser


class MarkdownDocument(pydantic.BaseModel):
    source: Optional[Path] = None

    blocks: List[AbstractBlock]

    def render(self) -> str:
        return '\n\n'.join(map(str, self.blocks))

    @classmethod
    def from_file(cls, path: Path) -> 'MarkdownDocument':
        file_content = path.read_text()
        return cls(blocks=cls.__parse_blocks(file_content), source=path)

    @classmethod
    def from_string(cls, text: str) -> 'MarkdownDocument':
        return cls(
            blocks=cls.__parse_blocks(text),
        )

    @staticmethod
    def __parse_blocks(text: str) -> List[AbstractBlock]:
        markdown_parser = mistune.create_markdown(renderer=TypedParser())
        data = [b for b in markdown_parser(text) if b and not isinstance(b, NewlineBlock)]
        return data
