import pytest

from md_translate.document.parser.blocks import (
    HeadingBlock,
    TextBlock,
    Paragraph,
    LineBreakBlock,
    StrongTextBlock,
    EmphasisTextBlock,
    LinkBlock,
    ImageBlock,
)
from md_translate.document.parser.document import MarkdownDocument

QUOTE = [
    '> Dorothy followed her through many of the beautiful rooms in her castle.',
    '''> Dorothy followed her through many of the beautiful rooms in her castle.
    >
    > The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.''',
    '''> #### The quarterly results look great!
    >
    > - Revenue was off the chart.
    > - Profits were higher than ever.
    >
    >  *Everything* is going according to **plan**.''',
]

ORDERED_LIST = [
    '''1. First item
2. Second item
3. Third item
4. Fourth item''',
    '''1. First item
1. Second item
1. Third item
1. Fourth item''',
    '''1. First item
8. Second item
3. Third item
5. Fourth item''',
    '''1. First item
2. Second item
3. Third item
    1. Indented item
    2. Indented item
4. Fourth item''',
]

UNORDERED_LIST = [
    '''- First item
- Second item
- Third item
- Fourth item''',
    '''* First item
* Second item
* Third item
* Fourth item''',
    '''+ First item
+ Second item
+ Third item
+ Fourth item''',
    '''- First item
- Second item
- Third item
    - Indented item
    - Indented item
- Fourth item''',
    '''- 1968\. A great year!
- I think 1969 was second best.''',
]

CODE = [
    'Use `code` in your Markdown file.',
    '``Use `code` in your Markdown file.``',
]

CODE_BLOCKS = [
    '''```python
def hello_world():
    print("Hello world!")
```''',
    '''```
def hello_world():
    print("Hello world!")
```''',
]

IMAGE = [
    '![The San Juan Mountains are beautiful!](/ assets / images / san-juan-mountains.jpg "San Juan Mountains")',
    '![Tux, the Linux mascot](https: // mdg.imgix.net / assets / images / tux.png)',
]

HORIZONTAL_LINE = [
    '***',
    '---',
    '_________________',
]


class TestMarkdownDocument:
    @pytest.mark.parametrize(
        'header, expected',
        [
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
        ],
    )
    def test_header_parsing(self, header, expected):
        assert MarkdownDocument.from_string(header).blocks == expected

    @pytest.mark.parametrize(
        'paragraph, expected',
        [
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
        ],
    )
    def test_paragraph_parsing(self, paragraph, expected):
        assert MarkdownDocument.from_string(paragraph).blocks == expected

    @pytest.mark.parametrize(
        'line_break, expected',
        [
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
            )
        ],
    )
    def test_line_break_parsing(self, line_break, expected):
        assert MarkdownDocument.from_string(line_break).blocks == expected

    @pytest.mark.parametrize(
        'bold, expected',
        [
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
        ],
    )
    def test_bold_parsing(self, bold, expected):
        assert MarkdownDocument.from_string(bold).blocks == expected

    @pytest.mark.parametrize(
        'italic, expected',
        [
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
            # todo: fix it
            (
                "This text is ***really important***.",
                [
                    Paragraph(
                        children=[
                            TextBlock(text='This text is *'),
                            StrongTextBlock(children=[TextBlock(text='really important')]),
                            TextBlock(text='*.'),
                        ]
                    )
                ],
            ),
        ],
    )
    def test_italic_parsing(self, italic, expected):
        assert MarkdownDocument.from_string(italic).blocks == expected

    @pytest.mark.parametrize(
        'link, expected',
        [
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
                'My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").',
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
        ],
    )
    def test_link_parsing(self, link, expected):
        assert MarkdownDocument.from_string(link).blocks == expected

    @pytest.mark.parametrize(
        'image, expected',
        [
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
        ],
    )
    def test_link_parsing(self, image, expected):
        assert MarkdownDocument.from_string(image).blocks == expected
