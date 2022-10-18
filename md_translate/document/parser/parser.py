from mistune.renderers import BaseRenderer

from . import blocks


class TypedParser(BaseRenderer):
    NAME = 'blocks'

    def text(self, text):
        print(f'text. {text=}')
        return blocks.TextBlock(text=text)

    def paragraph(self, children):
        return blocks.Paragraph(children=children)

    def block_text(self, text):
        return text
        # print(f'block_text. {text=}')
        # return blocks.TextBlock(text=text)

    def block_quote(self, children):
        return blocks.BlockQuote(children=children)

    def strong(self, children):
        return blocks.StrongTextBlock(children=children)

    def emphasis(self, children):
        return blocks.EmphasisTextBlock(children=children)

    def link(self, link, children=None, title=None):
        return blocks.LinkBlock(url=link, title=title, children=children)

    def image(self, url, alt="", title=None):
        return blocks.ImageBlock(url=url, alt=alt, title=title)

    def codespan(self, text):
        return blocks.CodeSpanBlock(code=text)

    def block_code(self, code, lang=None):
        return blocks.CodeBlock(code=code, language=lang)

    def heading(self, children, level):
        return blocks.HeadingBlock(level=level, children=children)

    def thematic_break(self):
        return blocks.SeparatorBlock()

    def linebreak(self):
        return blocks.LineBreakBlock()

    def newline(self):
        return blocks.NewlineBlock()

    def inline_html(self, html):
        return blocks.InlineHtmlBlock(code=html)

    def block_html(self, text):
        return blocks.HtmlBlock(code=text)

    def list(self, children, ordered, level=1, start=None):
        return blocks.ListBlock(children=children, ordered=ordered, level=level, start=start)

    def list_item(self, children, level=1):
        if isinstance(children, list) and isinstance(children[0], list):
            children = children[0]
        return blocks.ListItemBlock(children=children, level=level)

    def finalize(self, data):
        return list(data)
