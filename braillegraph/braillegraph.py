'''A library for creating graphs using Unicode braille characters'''

import argparse
import itertools


# The Unicode codepoint for an empty braille blocks (no raised dots)
_BRAILLE_EMPTY_BLOCK = 0x2800

# The offsets to add for dots. The dots are represented as an 8-bit bitfield as
# follows:
#
#     0x01  0x08
#     0x02  0x10
#     0x04  0x20
#     0x40  0x80
#
# Half rows only have a left-most dot. Full rows have both dots.
_BRAILLE_HALF_ROW = [0x01, 0x02, 0x04, 0x40]
_BRAILLE_FULL_ROW = [0x09, 0x12, 0x24, 0xC0]


def _chunk(iterable, size):
    '''Split an iterable into chunks of a fixed size.'''
    yield from (
        (item for index, item in group)
        for key, group in itertools.groupby(
            enumerate(iterable),
            lambda item: item[0] // size
        )
    )


def braillegraph(bars):
    '''Doc string'''
    lines = []

    # Break the bars into groups of four, one for each row in the braille
    # blocks.
    for bar_group in _chunk(bars, 4):
        line = []

        for braille_row, bar_value in enumerate(bar_group):
            # The number of full braille blocks needed to draw this bar. Each
            # block is two dots wide.
            full_blocks_needed = bar_value // 2

            # The number of braille blocks needed to draw this bar. The second
            # term accounts for a possible half row.
            blocks_needed = full_blocks_needed + (bar_value % 2)

            # The number of braille blocks we'll need to append to the current
            # line to accomodate this bar
            extra_blocks_needed = blocks_needed - len(line)

            # If we need extra blocks, add them.
            if extra_blocks_needed > 0:
                line.extend([_BRAILLE_EMPTY_BLOCK] * extra_blocks_needed)

            # Fill in the majority of the bar with full braille rows (two dots).
            for block_index in range(full_blocks_needed):
                line[block_index] += _BRAILLE_FULL_ROW[braille_row]

            # If the bar's value is odd, we'll need to add a single dot at the
            # end.
            if bar_value % 2:
                line[full_blocks_needed] += _BRAILLE_HALF_ROW[braille_row]

        # Wrap up this line by converting all the code points to characters
        # and concatenating them.
        lines.append(''.join(chr(code) for code in line))

    # Join all the lines to make the final graph
    return '\n'.join(lines)


def run():
    '''Display the arguments as a braille graph on standard output.'''

    # We override the program name to reflect that this script must be run with
    # the python executable.
    parser = argparse.ArgumentParser(
        prog='python braillegraph.py',
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

    args = parser.parse_args()

    print(braillegraph(args.integers), end=args.end)


if __name__ == '__main__':
    run()

