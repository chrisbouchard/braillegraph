"""A library for creating graphs using Unicode braille characters.

https://pypi.python.org/pypi/braillegraph

Someone on reddit posted a screenshot of their xmobar setup, which used braille
characters to show the loads of their four processor cores, as well as several
other metrics. I was impressed that you could fit so much data into a single
line. I immediately set out to implement braille bar graphs for myself.

The characters this script outputs are in the Unicode Braille Patterns section,
code points 0x2800 through 0x28FF. Not all fonts support these characters, so
if you can't see the examples below check your font settings.

There are two ways to use this package: imported in Python code, or as a
command line script.

To use the package in Python, import it and use the vertical_graph and
horizontal_graph functions.

    >>> from braillegraph import vertical_graph, horizontal_graph
    >>> vertical_graph([3, 1, 4, 1])
    '⡯⠥'
    >>> horizontal_graph([3, 1, 4, 1])
    '⣆⣇'

To use the package as a script, run it as

    % python -m braillegraph vertical 3 1 4 1 5 9 2 6
    ⡯⠥
    ⣿⣛⣓⠒⠂
    % python -m braillegraph horizontal 3 1 4 1 5 9 2 6
    ⠀⠀⢀
    ⠀⠀⣸⢠
    ⣆⣇⣿⣼

For a description of the arguments and flags, run

    % python -m braillegraph --help
"""

import argparse
from .braillegraph import horizontal_graph, vertical_graph


def run():
    """Display the arguments as a braille graph on standard output."""

    # We override the program name to reflect that this script must be run with
    # the python executable.
    parser = argparse.ArgumentParser(
        prog='python -m braillegraph',
        description='Print a braille bar graph of the given integers.'
    )

    # This flag sets the end string that we'll print. If we pass end=None to
    # print(), it will use its default. If we pass end='', it will suppress the
    # newline character.
    parser.add_argument('-n', '--no-newline', action='store_const',
                        dest='end', const='', default=None,
                        help='do not print the trailing newline character')

    # Add subparsers for the directions
    subparsers = parser.add_subparsers(title='directions')

    horizontal_parser = subparsers.add_parser('horizontal',
                                              help='a horizontal graph')
    horizontal_parser.set_defaults(
        func=lambda args: horizontal_graph(args.integers)
    )
    horizontal_parser.add_argument('integers', metavar='N', type=int,
                                   nargs='+', help='an integer')

    vertical_parser = subparsers.add_parser('vertical',
                                            help='a vertical graph')
    vertical_parser.set_defaults(
        func=lambda args: vertical_graph(args.integers, sep=args.sep)
    )
    vertical_parser.add_argument('integers', metavar='N', type=int, nargs='+',
                                 help='an integer')

    # The separator for groups of bars (i.e., "lines"). If we pass None,
    # vertical_parser will use its default.
    vertical_parser.add_argument('-s', '--sep', action='store', default=None,
                                 help='separator for groups of bars')

    args = parser.parse_args()

    print(args.func(args), end=args.end)


if __name__ == '__main__':
    run()

