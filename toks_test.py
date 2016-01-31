from toks import generate_tokens, name_tok, tok_name, untokenize
from io import StringIO


def test_name_tok():
    assert tok_name[-1] == 'WHITESPACE'


def test_add():
    toks = list(generate_tokens('a + b'))
    assert toks == [
        (0, 1, name_tok['NAME'], 'a'),
        (1, 2, name_tok['WHITESPACE'], ' '),
        (2, 3, name_tok['OP'], '+'),
        (3, 4, name_tok['WHITESPACE'], ' '),
        (4, 5, name_tok['NAME'], 'b'),
        (6, 6, name_tok['ENDMARKER'], ''),
    ]


def test_multi_line():
    program = '''from a import b

def c():
    b() + \
            5
class h(object):
    def hh(self):
        print('4')
print('h')'''

    assert_continuity_of_token_spans(program)
    assert_invariant(program)


def test_extra_newline_at_end():
    program = '''a = 4 # asdfasdf
'''
    assert_continuity_of_token_spans(program)
    assert_invariant(program)


def test_this_file():
    program = open(__file__, 'r').read()
    assert_continuity_of_token_spans(program)
    assert_invariant(program)


def assert_continuity_of_token_spans(program_text):
    current_position = 0
    program_text_length = len(program_text)
    for start, stop, tt, ts in generate_tokens(program_text):
        if start <= program_text_length:
            assert start == current_position
            current_position = stop
        else:
            assert tt == name_tok['ENDMARKER']


def assert_invariant(program_text):
    tokens = generate_tokens(program_text)
    f = StringIO()
    untokenize(tokens, f)
    f.seek(0)
    assert f.read() == program_text
