import ast

from unused import identify_unused


def test_identify_from_single():
    assert_identified_from([
    'from a import b'
    ], {'b'})

    assert_identified_from([
    'from a import b ',
    'print(b)',
    ], set())

    assert_identified_from([
    "print('hello')",
    'from a import b	 ',
    'a = b + 4',
    ], set())


def test_identify_from_multiple():
    assert_identified_from([
    'from a import b, c',
    ], {'b', 'c'})

    assert_identified_from([
    'from b import a',
    'from a import b, c ',
    ], {'a', 'b', 'c'})

    assert_identified_from([
    'from b import a',
    'from a import b, c ',
    'c()'
    ], {'a', 'b'})


def assert_identified_from(text_lines, expected_identified):
    text = '\n'.join(text_lines)
    tree = ast.parse(text)
    actual_identified = identify.identify_unused(tree)
    assert actual_identified == expected_identified
