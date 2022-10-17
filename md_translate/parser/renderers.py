from pathlib import Path
from typing import List

import mistune
from mistune.renderers import BaseRenderer

from md_translate.parser import blocks


class BlocksRenderer(BaseRenderer):
    NAME = 'blocks'

    def paragraph(self, children):
        if isinstance(children, list) and len(children) == 1:
            return children[0]
        if isinstance(children, blocks.TextBlock):
            return children
        if isinstance(children, list) and all(isinstance(child, blocks.TextBlock) for child in children):
            return blocks.TextBlock(''.join(str(child) for child in children))
        return blocks.RawDataBlock('paragraph', children)

    def block_text(self, text):
        return blocks.TextBlock(text)

    def text(self, text):
        return blocks.TextBlock(text)

    def strong(self, text):
        return blocks.TextBlock(text, strong=True)

    def emphasis(self, text):
        return blocks.TextBlock(text, emphasis=True)

    def link(self, link, text=None, title=None):
        text = self.maybe_join_text_blocks(text)
        return blocks.TextBlock(
            str(blocks.LinkBlock(link, title, text))
        )

    def image(self, src, alt="", title=None):
        return blocks.ImageBlock(src, alt, title)

    def codespan(self, text):
        return blocks.TextBlock(text)

    def heading(self, children, level):
        return blocks.HeadingBlock(level, children)

    def thematic_break(self):
        return blocks.SeparatorBlock()

    def block_code(self, code, lang=None):
        return blocks.CodeBlock(code, lang)

    def block_html(self, text):
        return blocks.HtmlBlock(text)

    def list(self, children, ordered, level, start=None):
        validated_children = []
        for child in children:
            if isinstance(child, blocks.ListItemBlock):
                validated_children.append(child)
            elif isinstance(child, list) and len(child) == 1 and isinstance(child[0], blocks.ListItemBlock):
                validated_children.append(child[0])
            else:
                validated_children.append(blocks.ListItemBlock(child))
        return blocks.ListBlock(validated_children, ordered)

    def list_item(self, children, level):
        if isinstance(children, list) and len(children) == 1:
            children = children[0]
        if isinstance(children, blocks.ListItemBlock):
            return children
        children = self.maybe_join_text_blocks(children)
        return blocks.ListItemBlock(children)

    def _create_default_method(self, name):
        def __raw(data=None):
            data = self.maybe_join_text_blocks(data)
            if data and isinstance(data, list) and len(data) == 1:
                return data[0]
            return blocks.RawDataBlock(name, data)

        return __raw

    def _get_method(self, name):
        try:
            return super(BlocksRenderer, self)._get_method(name)
        except AttributeError:
            return self._create_default_method(name)

    def finalize(self, data):
        return list(data)

    @staticmethod
    def maybe_join_text_blocks(blocks_):
        if not isinstance(blocks_, list):
            return blocks_
        if len(blocks_) == 1:
            return blocks_[0]
        if all(isinstance(block, blocks.TextBlock) for block in blocks_):
            return blocks.TextBlock(''.join(block.text for block in blocks_))
        return blocks
