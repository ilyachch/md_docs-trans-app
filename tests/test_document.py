import json
from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest
from md_translate.document.document import MarkdownDocument


class MockTranslator:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def translate(self, text):
        return f'{text}. translated'


TEST_DOCUMENT = '''# Test document

This is a test document.
'''


@pytest.fixture()
def test_document(tmp_path):
    temp_document = tmp_path / 'test.md'
    temp_document.write_text(TEST_DOCUMENT)
    try:
        yield temp_document
    finally:
        temp_document.unlink()


@pytest.fixture()
def test_document_with_cache(test_document):
    document = MarkdownDocument.from_file(test_document)
    document.cache()
    try:
        yield test_document
    finally:
        (test_document.parent / f'{test_document.name}.tmp').unlink()


class TestMarkdownDocument:
    @pytest.mark.parametrize(
        'file_path, expected_result',
        [
            (Path('tests/assets/test_document.md'), does_not_raise()),
            ('tests/assets/test_document.md', does_not_raise()),
            (Path('tests/assets/not_existing_document.md'), pytest.raises(FileNotFoundError)),
            ('tests/assets/not_existing_document.md', pytest.raises(FileNotFoundError)),
        ],
    )
    def test_loading(self, file_path, expected_result):
        with expected_result:
            MarkdownDocument.from_file(file_path)

    def test_dump(self):
        document = MarkdownDocument.from_file('tests/assets/simple_document.md')
        assert json.loads(document._dump_data()) == {
            'blocks': [
                {
                    'block_type': 'HeadingBlock',
                    'children': [{'block_type': 'TextBlock', 'text': 'Heading 1'}],
                    'level': 1,
                },
                {
                    'block_type': 'CodeBlock',
                    'code': 'def foo() -> bool:\n    return True',
                    'language': 'python',
                },
            ],
            'source': 'tests/assets/simple_document.md',
        }

    def test_load(self):
        document_dump = json.dumps(
            {
                'blocks': [
                    {
                        'block_type': 'HeadingBlock',
                        'children': [{'block_type': 'TextBlock', 'text': 'Heading 1'}],
                        'level': 1,
                    },
                    {
                        'block_type': 'CodeBlock',
                        'code': 'def foo() -> bool:\n    return True',
                        'language': 'python',
                    },
                ],
                'source': 'tests/assets/simple_document.md',
            }
        )
        document = MarkdownDocument(blocks=MarkdownDocument._load_data(document_dump))
        assert document.render() == Path('tests/assets/simple_document.md').read_text()

    def test_cache(self, test_document):
        document = MarkdownDocument.from_file(test_document)
        document.cache()
        assert (test_document.parent / f'{test_document.name}.tmp').exists()

    def test_restore(self, test_document_with_cache):
        document = MarkdownDocument.from_file(test_document_with_cache)
        document_restored = MarkdownDocument.restore(test_document_with_cache)
        assert document_restored == document

    @pytest.mark.parametrize(
        'document, params, expected_result',
        [
            (MarkdownDocument.from_string(TEST_DOCUMENT), {}, False),
            (
                MarkdownDocument.from_file('tests/assets/simple_document.md'),
                {'overwrite': True},
                True,
            ),
            (MarkdownDocument.from_file('tests/assets/simple_document.md'), {}, True),
            (
                MarkdownDocument.from_file('tests/assets/simple_document.md'),
                {'new_file': True},
                True,
            ),
            (MarkdownDocument.from_file('tests/assets/test_document.md'), {'new_file': True}, False),
            (MarkdownDocument.from_file('tests/assets/test_document_translated.md'), {}, False),
        ],
    )
    def test_should_be_translated(self, document, params, expected_result):
        assert document.should_be_translated(**params) == expected_result

    def test_translate(self, test_document):
        document = MarkdownDocument.from_file(test_document)
        document.translate(MockTranslator())  # type: ignore
        assert document.render_translated() == (
            "# Test document\n\n"
            "# Test document. translated\n\n"
            "This is a test document.\n\n"
            "This is a test document.. translated"
        )
        assert Path(test_document.parent / f'{test_document.name}.tmp').exists()

    def test_write(self, test_document):
        document = MarkdownDocument.from_file(test_document)
        document.translate(MockTranslator())
        document.write(translated=False)
        assert test_document.read_text() == TEST_DOCUMENT

    def test_write_translated(self, test_document):
        document = MarkdownDocument.from_file(test_document)
        document.translate(MockTranslator())
        document.write()
        assert test_document.read_text() == (
            '<!-- TRANSLATED by md-translate -->\n'
            "# Test document\n\n"
            "# Test document. translated\n\n"
            "This is a test document.\n\n"
            "This is a test document.. translated"
        )

    def test_write_new_file(self, test_document):
        document = MarkdownDocument.from_file(test_document)
        document.translate(MockTranslator())
        document.write(new_file=True)
        new_file = test_document.parent / f'{test_document.stem}_translated{test_document.suffix}'
        assert new_file.exists()
        assert new_file.read_text() == (
            '<!-- TRANSLATED by md-translate -->\n'
            '# Test document\n\n'
            '# Test document. translated\n\n'
            'This is a test document.\n\n'
            'This is a test document.. translated'
        )
