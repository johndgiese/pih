'''
This module is an extension of the `tokenize` module that takes into account
the precise formatting of whitespace.
'''
from io import StringIO
from tokenize import generate_tokens as _generate_tokens
from tokenize import tok_name as _tok_name

from lc_translator import build_lc_translator

tok_name = dict(_tok_name)
WHITESPACE = -1
tok_name[WHITESPACE] = 'WHITESPACE'

name_tok = {v:k for k, v in tok_name.items()}


def generate_tokens(program_text):
    non_ws_tokens = _generate_tokens(StringIO(program_text).readline)
    translator = build_lc_translator(program_text)

    current_position = 0

    for type, text, start_tup, stop_tup, _ in non_ws_tokens:
        start = translator(*start_tup)
        stop = translator(*stop_tup)
        if start != current_position and type != name_tok['ENDMARKER']:
            yield Token(current_position, start, WHITESPACE, program_text[current_position:start])
        current_position = stop
        yield Token(start, stop, type, text)


def untokenize(tokens, file):
    for t in tokens:
        print(t.text, file=file, end='')


class Token(object):
    def __init__(self, start, stop, token_type, text):
        self.start = start
        self.stop = stop
        self.text = text

        if type(token_type) == str:
            self.type = name_tok[token_type]
        else:
            self.type = token_type

    def __eq__(self, other):
        return self.start == other.start and self.text == other.text

    def __repr__(self):
        return '{} {}-{} "{}"'.format(tok_name[self.type], self.start, self.stop, self.text)
