from toks import generate_tokens, name_tok, tok_name, untokenize, Token
from io import StringIO


def test_name_tok():
    assert tok_name[-1] == 'WHITESPACE'


def test_add():
    toks = list(generate_tokens('a + b'))
    assert toks == [
        Token(0, 1, 'NAME', 'a'),
        Token(1, 2, 'WHITESPACE', ' '),
        Token(2, 3, 'OP', '+'),
        Token(3, 4, 'WHITESPACE', ' '),
        Token(4, 5, 'NAME', 'b'),
        Token(6, 6, 'ENDMARKER', ''),
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
    for token in generate_tokens(program_text):
        if token.start <= program_text_length:
            assert token.start == current_position
            current_position = token.stop
        else:
            assert token.type == name_tok['ENDMARKER']


def assert_invariant(program_text):
    tokens = generate_tokens(program_text)
    f = StringIO()
    untokenize(tokens, f)
    f.seek(0)
    assert f.read() == program_text
