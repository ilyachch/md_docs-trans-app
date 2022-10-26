import json
from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest
from md_translate.document.document import MarkdownDocument


@pytest.fixture()
def test_document(tmp_path):
    document_content = """
# Test document

This is a test document.
"""
    temp_document = tmp_path / 'test.md'
    temp_document.write_text(document_content)
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
