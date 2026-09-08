"""Release 9 regression contracts, including real CLI execution."""
import importlib
import itertools
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

from functools import partial

from slugify import slugify as public_slugify, smart_truncate

from slugify.__main__ import main, parse_args, slugify_params

slugify = partial(public_slugify, algorithm="modern")
core = importlib.import_module('slugify.slugify')


class ReleaseRegressionTests(unittest.TestCase):
    def test_legacy_goldens_and_differential(self):
        from tools import legacy_reference
        from tools.check_algorithms import check_differential, check_goldens
        check_goldens()
        self.assertEqual(check_differential(legacy_reference), 2688)

    def test_modern_separator_does_not_strip_word_content(self):
        for separator in ('x', 'xy', 'a', 'aa', '::', '', '-'):
            for text in ('xylophone x', 'xy xy', 'aaa a', 'a b c'):
                expected = separator.join(text.split())
                for boundary in (False, True):
                    self.assertEqual(slugify(text, separator=separator, max_length=100,
                                             word_boundary=boundary), expected)
                    for limit in range(1, len(expected) + 1):
                        actual = slugify(text, separator=separator, max_length=limit,
                                         word_boundary=boundary)
                        self.assertLessEqual(len(actual), limit)
        self.assertEqual(slugify('xylophone x', separator='x', max_length=1), 'x')
        self.assertEqual(slugify('xy xy', separator='xy', max_length=5), 'xyxyx')
        self.assertEqual(slugify('a b c', separator='::', max_length=3), 'a')

    def test_cli_preserves_legacy_default_shape(self):
        expected = dict(text='', entities=True, decimal=True, hexadecimal=True,
                        max_length=0, word_boundary=False, save_order=False, separator='-',
                        stopwords=None, lowercase=True, replacements=None, allow_unicode=False)
        for argv, overrides in (([], {}), (['Hello', '--no-lowercase'], {'text': 'Hello', 'lowercase': False})):
            with self.subTest(argv=argv):
                params = dict(expected, **overrides)
                args = parse_args(['slugify', *argv])
                namespace = dict(params, stdin=False, regex_pattern=None)
                namespace['input_string'] = namespace.pop('text')
                self.assertEqual(vars(args), namespace)
                self.assertEqual(slugify_params(args), params)
        with patch('slugify.__main__.slugify', return_value='') as call, patch('builtins.print'):
            main(['slugify'])
            call.assert_called_once_with(**expected)
        self.assertEqual(public_slugify('a&#39;b'), 'ab')

    def test_cli_explicit_options_are_forwarded(self):
        defaults = slugify_params(parse_args(['slugify']))
        for flag, values in (('--algorithm', ('legacy', 'modern')),
                             ('--backend', ('auto', 'text-unidecode', 'unidecode', 'anyascii')),
                             ('--replacement-stage', ('both', 'pre', 'post')),
                             ('--regex-pattern', ('', '[^a-z]+'))):
            for value in values:
                with self.subTest(flag=flag, value=value):
                    key = flag[2:].replace('-', '_')
                    args = parse_args(['slugify', flag, value])
                    expected = dict(defaults, **{key: value})
                    self.assertEqual(getattr(args, key), value)
                    self.assertEqual(slugify_params(args), expected)
                    with patch('slugify.__main__.slugify', return_value='') as call, patch('builtins.print'):
                        main(['slugify', flag, value])
                        call.assert_called_once_with(**expected)

    def test_algorithm_cli(self):
        for algorithm, expected in ((None, 'ab'), ('legacy', 'ab'), ('modern', 'a-b')):
            args = ['--algorithm', algorithm] if algorithm else []
            output = subprocess.check_output([sys.executable, '-m', 'slugify', *args, 'a&#39;b'], text=True)
            self.assertEqual(output, expected + '\n')
        result = subprocess.run([sys.executable, '-m', 'slugify', '--algorithm', 'invalid', 'a'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)

    def test_empty_and_whitespace(self):
        for text in ('', ' ', '\t\n', '\u2003\u00a0', '  \n\t  '):
            for unicode in (False, True):
                with self.subTest(text=text, unicode=unicode):
                    self.assertEqual(slugify(text, allow_unicode=unicode), '')

    def test_readme_examples(self):
        readme = Path(__file__).with_name('README.md').read_text(encoding='utf-8')
        for block in re.findall(r'```python\n(.*?)```', readme, flags=re.DOTALL):
            if block.startswith('slugify('):
                continue  # This block documents the signature, not an invocation.
            try:
                exec(compile(block, 'README.md', 'exec'), {})
            except ModuleNotFoundError as error:
                if error.name != 'text_unidecode':
                    raise  # The Unidecode isolation cell deliberately lacks this dependency.

    def test_bytes_and_replacements(self):
        for text in (b'caf\xc3\xa9\xff', bytearray(b'caf\xc3\xa9\xff')):
            self.assertEqual(slugify(text, replacements=[('c', 'k')]), 'kafe')
        for text in (None, 123, 1.2, [], {}, object()):
            with self.subTest(text=type(text)), self.assertRaisesRegex(TypeError, 'text must be'):
                slugify(text)

    def test_named_and_numeric_entities_match_literal_input(self):
        for unicode in (False, True):
            for encoded, literal in (('&#20320;', '你'), ('&#x4F60;', '你'),
                                     ('&beta;', 'β'), ('&#39;', "'"), ('&rsquo;', '’')):
                self.assertEqual(slugify('a ' + encoded + ' b', allow_unicode=unicode),
                                 slugify('a ' + literal + ' b', allow_unicode=unicode))

    def test_invalid_entities_do_not_cancel_neighbors(self):
        for unicode, letter in ((False, 'z'), (True, 'ž')):
            for invalid, expected in (('&#99999999999999999999;', '99999999999999999999'),
                                      ('&#x110000;', 'x110000'), ('&#55296;', '55296'),
                                      ('&#xDFFF;', 'xdfff')):
                self.assertEqual(slugify('&#381; ' + invalid + ' &#x17D;', allow_unicode=unicode),
                                 f'{letter}-{expected}-{letter}')
        # Exceeds Python's optional integer-string digit limit on newer runtimes.
        huge = '9' * 5000
        self.assertEqual(slugify('&#65; &#' + huge + '; &#66;'), 'a-' + huge + '-b')

    def test_entity_flags_are_independent(self):
        text = '&beta; &#65; &#x42;'
        self.assertEqual(slugify(text, entities=False, decimal=False, hexadecimal=False), 'beta-65-x42')
        self.assertEqual(slugify(text, entities=False, decimal=True, hexadecimal=False), 'beta-a-x42')
        self.assertEqual(slugify(text, entities=False, decimal=False, hexadecimal=True), 'beta-65-b')

    def test_normalization_ordinals_dashes_and_phonetic_quotes(self):
        self.assertEqual(slugify('1º 1ª 𝐚́́𝕒́'), '1o-1a-aa')
        self.assertEqual(slugify('a‐b‑c‒d–e—f'), 'a-b-c-d-e-f')
        self.assertEqual(slugify('ㅋ', allow_unicode=True), 'ᄏ')
        self.assertEqual(slugify("Baby's shoes"), 'baby-s-shoes')
        self.assertEqual(slugify('Baby’s shoes'), 'babys-shoes')
        self.assertEqual(slugify('Компьютер'), 'kompiuter')

    def test_replacement_stages_and_iterables(self):
        for stage, expected in (('both', 'aaaa'), ('pre', 'aa'), ('post', 'aa')):
            for rules in ([('a', 'aa')], iter([('a', 'aa')]), iter([iter(('a', 'aa'))])):
                self.assertEqual(slugify('a', replacements=rules, replacement_stage=stage), expected)
        self.assertEqual(slugify('a', replacements=[('a', 'b'), ('b', 'c')], replacement_stage='pre'), 'c')
        self.assertEqual(slugify('a', replacements=[('a', '!')], replacement_stage='post'), '!')
        self.assertEqual(slugify('a', replacements=[('a', '!')], replacement_stage='pre'), '')
        self.assertEqual(slugify('a', replacements=[('a', 'aaaa')], replacement_stage='post', max_length=2), 'aa')
        self.assertEqual(slugify('a', replacements=[('', 'x')], replacement_stage='pre'), 'xax')
        with self.assertRaises(ValueError):
            slugify('a', replacements=[('a', 'b', 'c')])
        with self.assertRaisesRegex(ValueError, 'replacement_stage'):
            slugify('a', replacement_stage='invalid')

    def test_stopword_iterators_case_sensitive_and_normalized(self):
        for lowercase, expected in ((True, 'b'), (False, 'a_B')):
            self.assertEqual(slugify('A a B', lowercase=lowercase, stopwords=iter(['A']), separator='_'),
                             expected)
        self.assertEqual(slugify('café b', stopwords=iter(['cafe'])), 'b')
        self.assertEqual(slugify('A a B', lowercase=False, stopwords=iter(['A'])), 'a-B')

    def test_actual_separator_width_and_literal_characters(self):
        self.assertEqual(slugify('a b c', separator='---', max_length=5), 'a---b')
        self.assertEqual(slugify('a b c', separator='---', max_length=3), 'a')
        self.assertEqual(slugify('a b c', separator='', max_length=2, word_boundary=True), 'ab')
        for separator in ('\\', r'\1', '[x]', '.*', '::', '---'):
            self.assertEqual(slugify('a b', separator=separator), 'a' + separator + 'b')
        # Legacy mapping intentionally still changes allowed literal dashes.
        self.assertEqual(slugify('a-b c', separator='_', regex_pattern=r'[^-a-z]+'), 'a_b_c')

    def test_empty_separator_preserves_word_boundaries(self):
        for order in (False, True):
            self.assertEqual(slugify('hello world', max_length=8, word_boundary=True,
                                    separator='', save_order=order), 'hello')
        self.assertEqual(slugify('oversized hi all', max_length=5, word_boundary=True,
                                separator=''), 'hiall')
        self.assertEqual(slugify('oversized hi all', max_length=5, word_boundary=True,
                                separator='', save_order=True), 'overs')
        self.assertEqual(slugify('a b', max_length=5, word_boundary=True, separator=''), 'ab')
        self.assertEqual(slugify('', max_length=5, word_boundary=True, separator=''), '')

    def test_truncate_contracts(self):
        self.assertEqual(smart_truncate(':alpha:', 0, separator='::'), 'alpha')
        self.assertEqual(smart_truncate('abcdef', -1), 'abcde')
        with self.assertRaises(ValueError):
            smart_truncate('abc', 2, True, '')
        self.assertEqual(smart_truncate('oversized a b', 3, True), 'a b')
        self.assertEqual(smart_truncate('oversized a b', 3, True, save_order=True), 'ove')

    def test_bounded_length_and_default_idempotence(self):
        corpus = ('', 'a b c', '影師嗎', 'A a B', "a's café", '1º—2ª', 'a___b', '&#65; &#x110000;')
        for text, separator, boundary, order, limit in itertools.product(
                corpus, ('-', '', '::', r'\1', 'aaa'), (False, True), (False, True), range(1, 12)):
            result = slugify(text, separator=separator, word_boundary=boundary, save_order=order, max_length=limit)
            self.assertLessEqual(len(result), limit)
        for text in corpus:
            result = slugify(text)
            self.assertEqual(slugify(result), result)

    def test_backend_selection_and_no_fallback_on_broken_install(self):
        with patch.object(core, 'import_module') as load:
            load.return_value.unidecode.return_value = 'chosen'
            self.assertEqual(slugify('x'), 'chosen')
            load.assert_called_once_with('unidecode')
        with patch.object(core, 'import_module', side_effect=ModuleNotFoundError(name='dependency')):
            with self.assertRaises(ModuleNotFoundError) as error:
                slugify('x')
            self.assertEqual(error.exception.name, 'dependency')
        with patch.object(core, 'import_module', side_effect=ModuleNotFoundError(name='anyascii')):
            with self.assertRaises(ModuleNotFoundError):
                slugify('x', backend='anyascii')
        with patch.object(core, 'import_module', side_effect=AssertionError('must not import')):
            self.assertEqual(slugify('影師嗎', allow_unicode=True, backend='anyascii'), '影師嗎')
        with self.assertRaisesRegex(ValueError, 'backend'):
            slugify('x', backend='invalid')

    def test_auto_falls_back_only_when_unidecode_missing(self):
        original = core.import_module

        def load(name):
            if name == 'unidecode':
                raise ModuleNotFoundError(name=name)
            return original(name)

        try:
            original('text_unidecode')
        except ModuleNotFoundError:
            self.skipTest('text-unidecode absent in isolated backend environment')
        with patch.object(core, 'import_module', side_effect=load):
            self.assertEqual(slugify('影師嗎'), 'ying-shi-ma')

    def test_explicit_backend_golden_corpus(self):
        corpus = ['影師嗎', 'Компьютер', 'β', 'café', '1º 1ª', '你']
        expected = {
            'text-unidecode': ['ying-shi-ma', 'kompiuter', 'b', 'cafe', '1o-1a', 'ni'],
            'unidecode': ['ying-shi-ma', 'kompiuter', 'b', 'cafe', '1o-1a', 'ni'],
            'anyascii': ['yingshima', 'kompyuter', 'v', 'cafe', '1o-1a', 'ni'],
        }
        for backend, values in expected.items():
            try:
                importlib.import_module(backend.replace('-', '_'))
            except ModuleNotFoundError:
                continue
            with self.subTest(backend=backend):
                self.assertEqual([slugify(text, backend=backend) for text in corpus], values)

    def test_cli_forwarding_and_real_module(self):
        argv = ['slugify', '--regex-pattern', '[^-a-z0-9_]+', '--backend', 'auto',
                '--replacement-stage', 'pre', '___This is a test___']
        params = slugify_params(parse_args(argv))
        self.assertEqual(params['regex_pattern'], '[^-a-z0-9_]+')
        self.assertEqual(params['backend'], 'auto')
        self.assertEqual(params['replacement_stage'], 'pre')
        result = subprocess.run([sys.executable, '-m', 'slugify', *argv[1:]],
                                check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout, '___this-is-a-test___\n')
        result = subprocess.run([sys.executable, '-m', 'slugify', '--stdin'], input='Café',
                                check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout, 'cafe\n')
        with patch('builtins.print') as output:
            main(argv)
            output.assert_called_once_with('___this-is-a-test___')
        with patch.object(sys, 'argv', ['slugify', 'Hello']), patch('builtins.print') as output:
            main()
            output.assert_called_once_with('hello')
        with patch('slugify.__main__.slugify', side_effect=KeyboardInterrupt), self.assertRaises(SystemExit):
            main(['slugify'])


if __name__ == '__main__':
    unittest.main()
