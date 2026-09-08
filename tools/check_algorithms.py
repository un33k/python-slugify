"""Reusable API compatibility checks, also run against installed release artifacts."""
import inspect
import itertools

from slugify import slugify, smart_truncate


def check_goldens():
    cases = (
        ('a&#39;b', {}, 'ab', 'a-b'),
        ('a&eacute;b', {}, 'ae-b', 'aeb'),
        ('a&#20320;b', {}, 'a-b', 'ani-b'),
        ('xylophone x', {'separator': 'x', 'max_length': 100}, 'xylophonexx', 'xylophonexx'),
        ('a b c', {'separator': '::', 'max_length': 3}, 'a::b', 'a'),
    )
    for text, options, legacy, modern in cases:
        assert slugify(text, **options) == legacy
        assert slugify(text, algorithm='legacy', **options) == legacy
        assert slugify(text, algorithm='modern', **options) == modern
    for algorithm, expected in (('legacy', 'aa'), ('modern', 'aaaa')):
        assert slugify('a', replacements=iter([('a', 'aa')]), algorithm=algorithm) == expected
    for algorithm, expected in (('legacy', 'a-b-a-b'), ('modern', 'a-a')):
        assert slugify('a b a b', stopwords=iter(['A', 'b']), lowercase=False, algorithm=algorithm) == expected
    parameter = inspect.signature(slugify).parameters['algorithm']
    assert parameter.kind == inspect.Parameter.KEYWORD_ONLY and parameter.default == 'legacy'
    try:
        slugify('a', algorithm='invalid')
    except ValueError:
        pass
    else:
        raise AssertionError('unknown algorithm accepted')


def check_differential(reference):
    corpus = ('', 'a b c', 'xylophone x', "Baby's café", 'a&eacute;b', 'a&#39;b', 'a&#20320;b',
              '&#65; &#99999999999999999999; &#66;', '&#x41; &#x110000; &#x42;',
              '&#55296;', '&#xDFFF;', '影師嗎', 'A a B', '1,234—5')
    count = 0
    for text, separator, limit, boundary, order, unicode in itertools.product(
            corpus, ('-', '', '::', 'x'), (0, -1, 1, 3, 8, 100), (False, True), (False, True), (False, True)):
        options = dict(separator=separator, max_length=limit, word_boundary=boundary,
                       save_order=order, allow_unicode=unicode)
        expected = reference.slugify(text, **options)
        assert slugify(text, **options) == expected, (text, options)
        assert slugify(text, algorithm='legacy', **options) == expected, (text, options)
        count += 1
    # Each call receives fresh iterators; using the same consumed object hides regressions.
    for replacements in (lambda: [('a', 'aa')], lambda: iter([('a', 'aa')]),
                         lambda: iter([iter(('a', 'aa'))])):
        assert slugify('a', replacements=replacements()) == reference.slugify('a', replacements=replacements())
    for lowercase in (False, True):
        assert slugify('a b a b', lowercase=lowercase, stopwords=iter(['A', 'b'])) == reference.slugify(
            'a b a b', lowercase=lowercase, stopwords=iter(['A', 'b']))
    for text, separator, limit, boundary, order in itertools.product(
            ('::alpha::', 'a b c', 'abcdef', ''), (' ', '::', '', 'x'), (0, -2, 1, 5), (False, True), (False, True)):
        args = (text, limit, boundary, separator, order)
        try:
            expected = reference.smart_truncate(*args)
        except ValueError:
            try:
                smart_truncate(*args)
            except ValueError:
                continue
            raise AssertionError(('missing legacy ValueError', args))
        assert smart_truncate(*args) == expected, args
    return count


if __name__ == '__main__':
    check_goldens()
    print('PASS: installed algorithm API goldens')
