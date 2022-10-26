import pytest

from md_translate.document.document import MarkdownDocument

HEADER_1 = r'# Heading level 1'

HEADER_2 = r'## Heading level 2'

HEADER_3 = r'### Heading level 3'

HEADER_4 = r'#### Heading level 4'

HEADER_5 = r'##### Heading level 5'

HEADER_6 = r'###### Heading level 6'

PARAGRAPH = r'''I really like using Markdown.

I think I'll use it to format all of my documents from now on.'''

NEW_LINE = 'This is the first line.  \nAnd this is the second line.'

BOLD_TEXT = 'I just love **bold text**.'

ITALIC_TEXT = "Italicized text is the *cat's meow*."

QUOTE = '> Dorothy followed her through many of the beautiful rooms in her castle.'

MULTILINE_QUOTE = r'''> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.'''

NESTED_QUOTE = r'''> Dorothy followed her through many of the beautiful rooms in her castle.
>
>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.'''

LIST_INSIDE_QUOTE = r'''> #### The quarterly results look great!
>
> * Revenue was off the chart.
> * Profits were higher than ever.
>
> *Everything* is going according to **plan**.'''

LIST = '''1. First item
2. Second item
3. Third item
    - Indented item
    - Indented item
4. Fourth item'''

LIST_WITH_NESTED_QUOTE = r'''* This is the first list item.
* Here's the second list item.
    > A blockquote would look great below the second list item.
* And here's the third list item.'''

IMAGE_LINK_WITH_TITLE = r'![The San Juan Mountains are beautiful!](/assets/images/san-juan-mountains.jpg "San Juan Mountains")'

IMAGE_LINK_WITHOUT_TITLE = (
    r'![The San Juan Mountains are beautiful!](/assets/images/san-juan-mountains.jpg)'
)

LINK_WITH_TITLE = r'[Visit our HTML tutorial!](/tutorials/html/ "HTML Tutorial")'

LINK_WITHOUT_TITLE = r'[Visit our HTML tutorial!](/tutorials/html/)'

SEPARATOR = r'---'

INLINE_HTML = r'<p>Raw HTML is not parsed.</p>'

MIXED_INLINE_HTML = 'This is a paragraph with <hr>'

HTML_BLOCK = r'<div class="footer">\n    &copy; 2004 Foo Corporation\n</div>'

CODE_SPAN = r'Use the `printf()` function.'

MARKDOWN_DOCUMENTS = [
    (HEADER_1, 'HEADER_1'),
    (HEADER_2, 'HEADER_2'),
    (HEADER_3, 'HEADER_3'),
    (HEADER_4, 'HEADER_4'),
    (HEADER_5, 'HEADER_5'),
    (HEADER_6, 'HEADER_6'),
    (PARAGRAPH, 'PARAGRAPH'),
    (NEW_LINE, 'NEW_LINE'),
    (BOLD_TEXT, 'BOLD_TEXT'),
    (ITALIC_TEXT, 'ITALIC_TEXT'),
    (QUOTE, 'QUOTE'),
    (MULTILINE_QUOTE, 'MULTILINE_QUOTE'),
    (NESTED_QUOTE, 'NESTED_QUOTE'),
    (LIST_INSIDE_QUOTE, 'LIST_INSIDE_QUOTE'),
    (LIST, 'LIST'),
    (LIST_WITH_NESTED_QUOTE, 'LIST_WITH_NESTED_QUOTE'),
    (IMAGE_LINK_WITH_TITLE, 'IMAGE_LINK_WITH_TITLE'),
    (IMAGE_LINK_WITHOUT_TITLE, 'IMAGE_LINK_WITHOUT_TITLE'),
    (LINK_WITH_TITLE, 'LINK_WITH_TITLE'),
    (LINK_WITHOUT_TITLE, 'LINK_WITHOUT_TITLE'),
    (SEPARATOR, 'SEPARATOR'),
    (INLINE_HTML, 'INLINE_HTML'),
    (MIXED_INLINE_HTML, 'MIXED_INLINE_HTML'),
    (HTML_BLOCK, 'HTML_BLOCK'),
    (CODE_SPAN, 'CODE_SPAN'),
]


@pytest.mark.parametrize(
    'document, _',
    [
        *MARKDOWN_DOCUMENTS,
        (
            '\n\n'.join([document for document, _ in MARKDOWN_DOCUMENTS]),
            'ALL',
        ),
    ],
    ids=[name for _, name in MARKDOWN_DOCUMENTS] + ['ALL'],
)
def test_rendering(document, _):
    md_document = MarkdownDocument.from_string(document)
    assert md_document.render() == document
