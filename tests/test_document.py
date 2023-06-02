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

```
def foo() -> bool:
    return True
```
'''

TEST_DOCUMENT_TRANSLATED = '''<!-- TRANSLATED by md-translate -->
# Test document

# Test document. translated

This is a test document.

This is a test document.. translated

```
def foo() -> bool:
    return True
```'''


@pytest.fixture()
def test_document(tmp_path):
    temp_document = tmp_path / 'test.md'
    temp_document.write_text(TEST_DOCUMENT)
    try:
        yield temp_document
    finally:
        temp_document.unlink()


@pytest.fixture()
def test_document_with_cache(test_document, test_settings):
    document = MarkdownDocument.from_file(test_document, settings=test_settings)
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
    def test_loading(self, file_path, expected_result, test_settings):
        with expected_result:
            MarkdownDocument.from_file(file_path, settings=test_settings)

    def test_dump(self, test_settings):
        document = MarkdownDocument.from_file(
            'tests/assets/simple_document.md', settings=test_settings
        )
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

    def test_load(self, test_settings):
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
        document = MarkdownDocument(
            blocks=MarkdownDocument._load_data(document_dump), settings=test_settings
        )
        assert document.render() == Path('tests/assets/simple_document.md').read_text()

    def test_cache(self, test_document, test_settings):
        document = MarkdownDocument.from_file(test_document, settings=test_settings)
        document.cache()
        assert (test_document.parent / f'{test_document.name}.tmp').exists()

    def test_restore(self, test_document_with_cache, test_settings):
        document = MarkdownDocument.from_file(test_document_with_cache, settings=test_settings)
        document_restored = MarkdownDocument.restore(
            test_document_with_cache, settings=test_settings
        )
        assert document_restored.blocks == document.blocks

    @pytest.mark.parametrize(
        'document_path, params, expected_result',
        [
            (
                'tests/assets/simple_document.md',
                {'overwrite': True},
                True,
            ),
            (
                'tests/assets/simple_document.md',
                {},
                True,
            ),
            (
                'tests/assets/simple_document.md',
                {'new_file': True},
                True,
            ),
            (
                'tests/assets/test_document.md',
                {'new_file': True},
                False,
            ),
            (
                'tests/assets/test_document_translated.md',
                {},
                False,
            ),
        ],
    )
    def test_should_be_translated(self, document_path, params, expected_result, test_settings):
        for key, value in params.items():
            setattr(test_settings, key, value)
        document = MarkdownDocument.from_file(document_path, settings=test_settings)
        assert document.should_be_translated() == expected_result

    def test_should_be_translated_from_string(self, test_settings):
        document = MarkdownDocument.from_string(TEST_DOCUMENT, settings=test_settings)
        assert document.should_be_translated() is False

    @pytest.mark.parametrize(
        'drop_original',
        [True, False],
    )
    def test_translate(self, test_document, drop_original, test_settings):
        test_settings.drop_original = drop_original
        document = MarkdownDocument.from_file(test_document, settings=test_settings)
        document.translate(MockTranslator())  # type: ignore
        if drop_original:
            assert document.render_translated() == (
                '# Test document. translated\n'
                '\n'
                'This is a test document.. translated\n'
                '\n'
                '```\n'
                'def foo() -> bool:\n'
                '    return True\n'
                '```'
            )
        else:
            assert document.render_translated() == (
                '# Test document\n'
                '\n'
                '# Test document. translated\n'
                '\n'
                'This is a test document.\n'
                '\n'
                'This is a test document.. translated\n'
                '\n'
                '```\n'
                'def foo() -> bool:\n'
                '    return True\n'
                '```'
            )
        assert Path(test_document.parent / f'{test_document.name}.tmp').exists()

    def test_write(self, test_document, test_settings):
        document = MarkdownDocument.from_file(test_document, settings=test_settings)
        document.translate(MockTranslator())
        document.write()
        assert test_document.read_text() == TEST_DOCUMENT_TRANSLATED

    def test_write_translated(self, test_document, test_settings):
        document = MarkdownDocument.from_file(test_document, settings=test_settings)
        document.translate(MockTranslator())
        document.write()
        assert test_document.read_text() == TEST_DOCUMENT_TRANSLATED

    def test_write_new_file(self, test_document, test_settings):
        test_settings.new_file = True
        document = MarkdownDocument.from_file(test_document, settings=test_settings)
        document.translate(MockTranslator())
        document.write()
        new_file = test_document.parent / f'{test_document.stem}_translated{test_document.suffix}'
        assert new_file.exists()
        assert new_file.read_text() == TEST_DOCUMENT_TRANSLATED
