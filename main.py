#!/usr/bin/python
import argparse
import ast

from unused import identify_unused


parser = argparse.ArgumentParser(description='The Python import helper.')

parser.add_argument('files', metavar='file', type=str, nargs='+',
        help='python file to process')
parser.add_argument('-u', '--unused', dest='remove_unused', action='store_true', 
        help='remove unused imports (default')


if __name__ == '__main__':
    args = parser.parse_args()
    for fn in args.files:
        f = open(fn, 'r')
        text = f.read()
        tree = ast.parse(text)
        unused = identify_unused(tree)
        if unused:
            print('')
            print(fn)
            print(unused)
