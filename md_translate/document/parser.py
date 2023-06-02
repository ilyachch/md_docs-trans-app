from typing import Any, List

from mistune.renderers import BaseRenderer

from md_translate.document import blocks


class TypedParser(BaseRenderer):
    NAME = 'blocks'

    def text(self, text: str) -> blocks.TextBlock:
        return blocks.TextBlock(text=text)

    def paragraph(self, children: List[blocks.BaseBlock]) -> blocks.Paragraph:
        return blocks.Paragraph(children=children)

    def block_text(self, text: str) -> str:
        return text

    def block_quote(self, children: List[blocks.BaseBlock]) -> blocks.BlockQuote:
        if children and isinstance(children[0], list) and len(children) == 1:
            children = children[0]
        prepared_children = []
        for i, child in enumerate(children):
            prepared_children.append(child)
            if i + 1 < len(children):
                prepared_children.append(blocks.NewlineBlock())

        return blocks.BlockQuote(children=prepared_children)

    def strong(self, children: List[blocks.BaseBlock]) -> blocks.StrongTextBlock:
        return blocks.StrongTextBlock(children=children)

    def emphasis(self, children: List[blocks.BaseBlock]) -> blocks.EmphasisTextBlock:
        return blocks.EmphasisTextBlock(children=children)

    def link(
        self, link: str, children: List[blocks.BaseBlock] = None, title: str = None
    ) -> blocks.LinkBlock:
        return blocks.LinkBlock(url=link, title=title, children=children)

    def image(self, url: str, alt: str = "", title: str = None) -> blocks.ImageBlock:
        return blocks.ImageBlock(url=url, alt=alt, title=title)

    def codespan(self, text: str) -> blocks.CodeSpanBlock:
        return blocks.CodeSpanBlock(code=text)

    def block_code(self, code: str, lang: str = None) -> blocks.CodeBlock:
        return blocks.CodeBlock(code=code, language=lang)

    def heading(self, children: List[blocks.BaseBlock], level: int) -> blocks.HeadingBlock:
        return blocks.HeadingBlock(level=level, children=children)

    def thematic_break(self) -> blocks.SeparatorBlock:
        return blocks.SeparatorBlock()

    def linebreak(self) -> blocks.LineBreakBlock:
        return blocks.LineBreakBlock()

    def newline(self) -> blocks.NewlineBlock:
        return blocks.NewlineBlock()

    def inline_html(self, html: str) -> blocks.HtmlBlock:
        return blocks.InlineHtmlBlock(code=html)

    def block_html(self, text: str) -> blocks.HtmlBlock:
        return blocks.HtmlBlock(code=text)

    def list(
        self,
        children: List[blocks.ListItemBlock],
        ordered: bool,
        level: int = 1,
        start: int = None,
    ) -> blocks.ListBlock:
        if ordered:
            start = start or 1
        return blocks.ListBlock(children=children, ordered=ordered, level=level, start=start)

    def list_item(
        self, children: tuple[List[blocks.BaseBlock], blocks.BaseBlock], level: int = 1
    ) -> blocks.ListItemBlock:
        base_children: List[blocks.BaseBlock] = children[0]
        if not isinstance(base_children, list):
            base_children = [base_children]  # type: ignore  # pragma: no cover
        nested_children: List[blocks.BaseBlock] = list(children[1:]) if len(children) > 1 else []
        flattened_children: list[blocks.BaseBlock] = []
        for child in nested_children:
            if isinstance(child, list):
                flattened_children.extend(child)
            else:
                flattened_children.append(child)
        return blocks.ListItemBlock(
            children=base_children, nested_children=flattened_children, level=level
        )

    def finalize(self, data: Any) -> List:
        return list(data)
