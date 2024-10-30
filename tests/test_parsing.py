from typing import Generator, Tuple

import pytest

from md_translate.document.blocks import (
    BlockQuote,
    CodeBlock,
    CodeSpanBlock,
    EmphasisTextBlock,
    HeadingBlock,
    HtmlBlock,
    ImageBlock,
    InlineHtmlBlock,
    LineBreakBlock,
    LinkBlock,
    ListBlock,
    ListItemBlock,
    NewlineBlock,
    Paragraph,
    SeparatorBlock,
    StrongTextBlock,
    TextBlock,
)
from md_translate.document.document import MarkdownDocument


def _params_shortener(*params, id_name) -> Generator[Tuple[str, ...], None, None]:
    for num, param in enumerate(params):
        yield pytest.param(*param, id=f'{id_name}_{num}')


class TestMarkdownParsing:
    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '# Heading level 1',
                [HeadingBlock(children=[TextBlock(text='Heading level 1')], level=1)],
            ),
            (
                '## Heading level 2',
                [HeadingBlock(children=[TextBlock(text='Heading level 2')], level=2)],
            ),
            (
                '### Heading level 3',
                [HeadingBlock(children=[TextBlock(text='Heading level 3')], level=3)],
            ),
            (
                '#### Heading level 4',
                [HeadingBlock(children=[TextBlock(text='Heading level 4')], level=4)],
            ),
            (
                '##### Heading level 5',
                [HeadingBlock(children=[TextBlock(text='Heading level 5')], level=5)],
            ),
            (
                '###### Heading level 6',
                [HeadingBlock(children=[TextBlock(text='Heading level 6')], level=6)],
            ),
            id_name='heading',
        ),
    )
    def test_header_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                'I really like using Markdown.',
                [Paragraph(children=[TextBlock(text='I really like using Markdown.')])],
            ),
            (
                "I think I'll use it to format all of my documents from now on.",
                [
                    Paragraph(
                        children=[
                            TextBlock(
                                text="I think I'll use it to format all of my documents from now on."
                            )
                        ]
                    )
                ],
            ),
            (
                '''I really like using Markdown.\n\nI think I'll use it to format all of my documents from now on.''',
                [
                    Paragraph(children=[TextBlock(text='I really like using Markdown.')]),
                    Paragraph(
                        children=[
                            TextBlock(
                                text="I think I'll use it to format all of my documents from now on."
                            )
                        ]
                    ),
                ],
            ),
            id_name='paragraph',
        ),
    )
    def test_paragraph_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                'This is the first line.  \nAnd this is the second line.',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='This is the first line.'),
                            LineBreakBlock(),
                            TextBlock(text='And this is the second line.'),
                        ]
                    )
                ],
            ),
            id_name='line_break',
        ),
    )
    def test_line_break_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                'I just love **bold text**.',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='I just love '),
                            StrongTextBlock(children=[TextBlock(text='bold text')]),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            (
                'I just love __bold text__.',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='I just love '),
                            StrongTextBlock(children=[TextBlock(text='bold text')]),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            (
                'Love**is**bold',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='Love'),
                            StrongTextBlock(children=[TextBlock(text='is')]),
                            TextBlock(text='bold'),
                        ]
                    )
                ],
            ),
            id_name='bold',
        ),
    )
    def test_bold_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                "Italicized text is the *cat's meow*.",
                [
                    Paragraph(
                        children=[
                            TextBlock(text='Italicized text is the '),
                            EmphasisTextBlock(children=[TextBlock(text="cat's meow")]),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            (
                "Italicized text is the _cat's meow_.",
                [
                    Paragraph(
                        children=[
                            TextBlock(text='Italicized text is the '),
                            EmphasisTextBlock(children=[TextBlock(text="cat's meow")]),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            (
                "This text is **_really important_**.",
                [
                    Paragraph(
                        children=[
                            TextBlock(text='This text is '),
                            StrongTextBlock(
                                children=[
                                    EmphasisTextBlock(
                                        children=[TextBlock(text='really important')]
                                    )
                                ]
                            ),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            (
                "This text is *__really important__*.",
                [
                    Paragraph(
                        children=[
                            TextBlock(text='This text is '),
                            EmphasisTextBlock(
                                children=[
                                    StrongTextBlock(children=[TextBlock(text='really important')])
                                ]
                            ),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            id_name='italic',
        ),
    )
    def test_italic_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                'My favorite search engine is [Duck Duck Go](https://duckduckgo.com).',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='My favorite search engine is '),
                            LinkBlock(
                                children=[TextBlock(text='Duck Duck Go')],
                                url='https://duckduckgo.com',
                            ),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            (
                'My favorite search engine is [Duck Duck Go]'
                '(https://duckduckgo.com "The best search engine for privacy").',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='My favorite search engine is '),
                            LinkBlock(
                                children=[TextBlock(text='Duck Duck Go')],
                                url='https://duckduckgo.com',
                                title='The best search engine for privacy',
                            ),
                            TextBlock(text='.'),
                        ]
                    )
                ],
            ),
            id_name='link',
        ),
    )
    def test_link_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '![The San Juan Mountains are beautiful!](/assets/images/san-juan-mountains.jpg "San Juan Mountains")',
                [
                    Paragraph(
                        children=[
                            ImageBlock(
                                alt='The San Juan Mountains are beautiful!',
                                url='/assets/images/san-juan-mountains.jpg',
                                title='San Juan Mountains',
                            ),
                        ]
                    )
                ],
            ),
            (
                '![Tux, the Linux mascot](https://mdg.imgix.net/assets/images/tux.png)',
                [
                    Paragraph(
                        children=[
                            ImageBlock(
                                alt='Tux, the Linux mascot',
                                url='https://mdg.imgix.net/assets/images/tux.png',
                            ),
                        ]
                    )
                ],
            ),
            id_name='image',
        ),
    )
    def test_images_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '---',
                [
                    SeparatorBlock(),
                ],
            ),
            (
                '***',
                [
                    SeparatorBlock(),
                ],
            ),
            (
                '___',
                [
                    SeparatorBlock(),
                ],
            ),
            id_name='separator',
        ),
    )
    def test_separator_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '```python\ndef hello_world():\n    print("Hello world!")\n```',
                [
                    CodeBlock(
                        language='python', code='def hello_world():\n    print("Hello world!")\n'
                    ),
                ],
            ),
            (
                '```\ndef hello_world():\n    print("Hello world!")\n```',
                [
                    CodeBlock(
                        language=None, code='def hello_world():\n    print("Hello world!")\n'
                    ),
                ],
            ),
            id_name='code',
        ),
    )
    def test_code_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                'Use `code` in your Markdown file.',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='Use '),
                            CodeSpanBlock(code='code'),
                            TextBlock(text=' in your Markdown file.'),
                        ]
                    )
                ],
            ),
            (
                '``Use `code` in your Markdown file.``',
                [Paragraph(children=[CodeSpanBlock(code='Use `code` in your Markdown file.')])],
            ),
            id_name='code_line',
        ),
    )
    def test_code_line_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '1. First item\n2. Second item\n3. Third item\n4. Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(children=[TextBlock(text='First item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Second item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Third item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Fourth item')], level=1),
                        ],
                        ordered=True,
                        level=1,
                        start=1,
                    )
                ],
            ),
            (
                '1. First item\n1. Second item\n1. Third item\n1. Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(children=[TextBlock(text='First item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Second item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Third item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Fourth item')], level=1),
                        ],
                        ordered=True,
                        level=1,
                        start=1,
                    )
                ],
            ),
            (
                '1. First item\n8. Second item\n3. Third item\n5. Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(children=[TextBlock(text='First item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Second item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Third item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Fourth item')], level=1),
                        ],
                        ordered=True,
                        level=1,
                        start=1,
                    )
                ],
            ),
            (
                '1. First item\n2. Second item\n3. Third item\n    1. Indented item\n    2. Indented item\n4. Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(
                                children=[TextBlock(text='First item')],
                                nested_children=[],
                                level=1,
                            ),
                            ListItemBlock(
                                children=[TextBlock(text='Second item')],
                                nested_children=[],
                                level=1,
                            ),
                            ListItemBlock(
                                children=[TextBlock(text='Third item')],
                                nested_children=[
                                    ListBlock(
                                        children=[
                                            ListItemBlock(
                                                children=[TextBlock(text='Indented item')],
                                                nested_children=[],
                                                level=2,
                                            ),
                                            ListItemBlock(
                                                children=[TextBlock(text='Indented item')],
                                                nested_children=[],
                                                level=2,
                                            ),
                                        ],
                                        ordered=True,
                                        level=2,
                                        start=1,
                                    )
                                ],
                                level=1,
                            ),
                            ListItemBlock(
                                children=[TextBlock(text='Fourth item')],
                                nested_children=[],
                                level=1,
                            ),
                        ],
                        ordered=True,
                        level=1,
                        start=1,
                    )
                ],
            ),
            id_name='ordered_list',
        ),
    )
    def test_ordered_list_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '- First item\n- Second item\n- Third item\n- Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(children=[TextBlock(text='First item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Second item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Third item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Fourth item')], level=1),
                        ],
                        ordered=False,
                        level=1,
                    )
                ],
            ),
            (
                '* First item\n* Second item\n* Third item\n* Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(children=[TextBlock(text='First item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Second item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Third item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Fourth item')], level=1),
                        ],
                        ordered=False,
                        level=1,
                    )
                ],
            ),
            (
                '+ First item\n+ Second item\n+ Third item\n+ Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(children=[TextBlock(text='First item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Second item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Third item')], level=1),
                            ListItemBlock(children=[TextBlock(text='Fourth item')], level=1),
                        ],
                        ordered=False,
                        level=1,
                    )
                ],
            ),
            (
                '- First item\n- Second item\n- Third item\n    - Indented item\n    - Indented item\n- Fourth item',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(
                                children=[TextBlock(text='First item')],
                                nested_children=[],
                                level=1,
                            ),
                            ListItemBlock(
                                children=[TextBlock(text='Second item')],
                                nested_children=[],
                                level=1,
                            ),
                            ListItemBlock(
                                children=[TextBlock(text='Third item')],
                                nested_children=[
                                    ListBlock(
                                        children=[
                                            ListItemBlock(
                                                children=[TextBlock(text='Indented item')],
                                                nested_children=[],
                                                level=2,
                                            ),
                                            ListItemBlock(
                                                children=[TextBlock(text='Indented item')],
                                                nested_children=[],
                                                level=2,
                                            ),
                                        ],
                                        ordered=False,
                                        level=2,
                                    )
                                ],
                                level=1,
                            ),
                            ListItemBlock(
                                children=[TextBlock(text='Fourth item')],
                                nested_children=[],
                                level=1,
                            ),
                        ],
                        ordered=False,
                        level=1,
                    )
                ],
            ),
            (
                '- 1968 - A great year!\n- I think 1969 was second best.',
                [
                    ListBlock(
                        children=[
                            ListItemBlock(
                                children=[
                                    TextBlock(text='1968 - A great year!'),
                                ],
                                level=1,
                            ),
                            ListItemBlock(
                                children=[
                                    TextBlock(text='I think 1969 was second best.'),
                                ],
                                level=1,
                            ),
                        ],
                        ordered=False,
                        level=1,
                    )
                ],
            ),
            (
                '- first\n- second\n    - third\n  second addition',
                [
                    ListBlock(
                        translated_data=None,
                        children=[
                            ListItemBlock(
                                translated_data=None,
                                children=[TextBlock(translated_data=None, text='first')],
                                nested_children=[],
                                level=1,
                            ),
                            ListItemBlock(
                                translated_data=None,
                                children=[TextBlock(translated_data=None, text='second')],
                                nested_children=[
                                    ListBlock(
                                        translated_data=None,
                                        children=[
                                            ListItemBlock(
                                                translated_data=None,
                                                children=[
                                                    TextBlock(translated_data=None, text='third')
                                                ],
                                                nested_children=[],
                                                level=2,
                                            )
                                        ],
                                        ordered=False,
                                        level=2,
                                        start=None,
                                    ),
                                    TextBlock(translated_data=None, text='second addition'),
                                ],
                                level=1,
                            ),
                        ],
                        ordered=False,
                        level=1,
                        start=None,
                    )
                ],
            ),
            id_name='unordered_list',
        ),
    )
    def test_unordered_list_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '> Dorothy followed her through many of the beautiful rooms in her castle.',
                [
                    BlockQuote(
                        children=[
                            Paragraph(
                                children=[
                                    TextBlock(
                                        text='Dorothy followed her through many of the beautiful rooms in her castle.'
                                    )
                                ]
                            )
                        ]
                    )
                ],
            ),
            (
                '> Dorothy followed her through many of the beautiful rooms in her castle.\n>\n>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.',
                [
                    BlockQuote(
                        children=[
                            Paragraph(
                                children=[
                                    TextBlock(
                                        text='Dorothy followed her through many of the beautiful rooms in her castle.'
                                    )
                                ]
                            ),
                            NewlineBlock(),
                            BlockQuote(
                                children=[
                                    Paragraph(
                                        children=[
                                            TextBlock(
                                                text='The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.'
                                            )
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                ],
            ),
            (
                '> Dorothy followed her through many of the beautiful rooms in her castle.\n>\n> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.',
                [
                    BlockQuote(
                        children=[
                            Paragraph(
                                children=[
                                    TextBlock(
                                        text='Dorothy followed her through many of the beautiful rooms in her castle.'
                                    )
                                ]
                            ),
                            NewlineBlock(),
                            Paragraph(
                                children=[
                                    TextBlock(
                                        text='The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.'
                                    )
                                ]
                            ),
                        ]
                    )
                ],
            ),
            (
                '> #### The quarterly results look great!\n>\n> - Revenue was off the chart.\n> - Profits were higher than ever.\n>\n>  *Everything* is going according to **plan**.',
                [
                    BlockQuote(
                        children=[
                            HeadingBlock(
                                children=[
                                    TextBlock(text='The quarterly results look great!'),
                                ],
                                level=4,
                            ),
                            NewlineBlock(),
                            ListBlock(
                                children=[
                                    ListItemBlock(
                                        children=[
                                            TextBlock(text='Revenue was off the chart.'),
                                        ],
                                        level=1,
                                    ),
                                    ListItemBlock(
                                        children=[
                                            TextBlock(text='Profits were higher than ever.')
                                        ],
                                        level=1,
                                    ),
                                ],
                                ordered=False,
                                level=1,
                            ),
                            NewlineBlock(),
                            Paragraph(
                                children=[
                                    EmphasisTextBlock(
                                        children=[
                                            TextBlock(text='Everything'),
                                        ]
                                    ),
                                    TextBlock(text=' is going according to '),
                                    StrongTextBlock(
                                        children=[
                                            TextBlock(text='plan'),
                                        ]
                                    ),
                                    TextBlock(text='.'),
                                ]
                            ),
                        ]
                    )
                ],
            ),
            id_name='quote',
        ),
    )
    def test_quote_parsing(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                'This is a paragraph with <hr>',
                [
                    Paragraph(
                        children=[
                            TextBlock(text='This is a paragraph with '),
                            InlineHtmlBlock(code='<hr>'),
                        ]
                    )
                ],
            ),
            id_name='inline_html',
        ),
    )
    def test_inline_html(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

    @pytest.mark.parametrize(
        'text, expected',
        _params_shortener(
            (
                '<div>\n\t<p>This is a paragraph with <hr></p>\n</div>',
                [
                    HtmlBlock(code='<div>\n    <p>This is a paragraph with <hr></p>\n</div>'),
                ],
            ),
            id_name='html_code',
        ),
    )
    def test_html_code(self, text, expected, test_settings):
        doc = MarkdownDocument.from_string(text, settings=test_settings)
        assert doc.blocks == expected
        assert (
            MarkdownDocument.from_string(doc.render(), settings=test_settings).blocks == doc.blocks
        )

