from mistune.renderers import BaseRenderer

from md_translate.document import _blocks as blocks


class BlocksRenderer(BaseRenderer):
    NAME = 'blocks'

    def paragraph(self, children):
        try:
            return blocks.TextBlock(text=' '.join(str(child) for child in children))
        except ValueError:
            return blocks.RawDataBlock(name='paragraph', data=children)

    def block_text(self, text):
        return blocks.TextBlock(text=text)

    def text(self, text):
        return blocks.TextBlock(text=text)

    def strong(self, text):
        return blocks.StrongTextBlock(text=text)

    def emphasis(self, text):
        return blocks.EmphasisTextBlock(text=text)

    def link(self, link, text=None, title=None):
        return blocks.TextBlock(text=str(blocks.LinkBlock(link=link, title=title, text=text)))

    def image(self, src, alt="", title=None):
        return blocks.ImageBlock(src=src, alt=alt, title=title)

    def codespan(self, text):
        return blocks.TextBlock(text=text)

    def heading(self, children, level):
        return blocks.HeadingBlock(level=level, text=' '.join(str(child) for child in children))

    def thematic_break(self):
        return blocks.SeparatorBlock()

    def block_code(self, code, lang=None):
        return blocks.CodeBlock(code=code, language=lang)

    def block_html(self, text):
        return blocks.HtmlBlock(code=text)

    def list(self, children, ordered, level, start=None):
        return blocks.ListBlock(children=children, ordered=ordered)

    def list_item(self, children, level):
        return blocks.ListItemBlock(children=children)

    def _create_default_method(self, name):
        def __raw(data=None):
            if data and isinstance(data, list) and len(data) == 1:
                return data[0]
            return blocks.RawDataBlock(name=name, data=data)

        return __raw

    def _get_method(self, name):
        try:
            return super(BlocksRenderer, self)._get_method(name)
        except AttributeError:
            return self._create_default_method(name)

    def finalize(self, data):
        return list(data)
