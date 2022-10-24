import json
from contextlib import nullcontext as does_not_raise
from pathlib import Path
from unittest.mock import patch

import pytest
from md_translate.document.parser.document import MarkdownDocument


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

    @pytest.mark.parametrize(
        'data, expected_result',
        [
            ('# Test', does_not_raise()),
            ('', pytest.raises(ValueError)),
        ],
    )
    def test_loading_string(self, data, expected_result):
        with expected_result:
            MarkdownDocument.from_string(data)

    def test_dump(self):
        document = MarkdownDocument.from_file('tests/assets/simple_document.md')
        assert json.loads(document.dump()) == {
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
        document = MarkdownDocument(blocks=[], allow_empty=True)
        document.load(document_dump)
        assert document.render() == Path('tests/assets/simple_document.md').read_text()
