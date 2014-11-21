'''A library for creating graphs using Unicode braille characters'''

import argparse
from . import braillegraph


def run():
    '''Display the arguments as a braille graph on standard output.'''

    # We override the program name to reflect that this script must be run with
    # the python executable.
    parser = argparse.ArgumentParser(
        prog='python -m braillegraph',
        description='Print a braille bar graph of the given integers.'
    )

    # Convert positional arguments to integers.
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer')

    # This flag sets the end string that we'll print. If we pass end=None to
    # print(), it will use its default. If we pass end='', it will suppress the
    # newline character.
    parser.add_argument('-n', '--no-newline', action='store_const',
                        dest='end', const='', default=None,
                        help='do not print the trailing newline character')

    # The separator for groups of bars (i.e., "lines"). If we pass None,
    # braillegraph will use its default.
    parser.add_argument('-s', '--sep', action='store', default=None,
                        help='separator for groups of bars')

    args = parser.parse_args()

    print(braillegraph(args.integers, sep=args.sep), end=args.end)


if __name__ == '__main__':
    run()

