'''
This module is an extension of the `tokenize` module that takes into account
the precise formatting of whitespace.  Note that the format of the token tuple
is somewhat different.
'''
from io import StringIO
from tokenize import generate_tokens as _generate_tokens
from tokenize import tok_name as _tok_name

from lc_translator import build_lc_translator

tok_name = dict(_tok_name)
tok_name[-1] = 'WHITESPACE'

name_tok = {v:k for k, v in tok_name.items()}


def generate_tokens(text):
    non_ws_tokens = _generate_tokens(StringIO(text).readline)
    translator = build_lc_translator(text)

    current_position = 0

    for tt, ts, start_tup, stop_tup, _ in non_ws_tokens:
        start = translator(*start_tup)
        stop = translator(*stop_tup)
        if start != current_position and tt != name_tok['ENDMARKER']:
            yield current_position, start, -1, text[current_position:start]
        current_position = stop
        yield start, stop, tt, ts


def untokenize(tokens, file):
    for _, _, _, ts in tokens:
        print(ts, file=file, end='')
