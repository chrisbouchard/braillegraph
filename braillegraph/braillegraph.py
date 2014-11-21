'''A library for creating graphs using Unicode braille characters

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

To use the package in Python, import it and use the braillegraph function.

    >>> from braillegraph import braillegraph
    >>> braillegraph([1, 2, 3, 4])
    '⣷⣄'

To use the package as a script, run it as

    % python -m braillegraph 1 2 3 4 5 6
    ⣷⣄
    ⠛⠛⠓

For a description of the arguments and flags, run

    % python -m braillegraph --help
'''

import itertools


# Only export this function. Everything else is an implementation detail.
__all__ = ['braillegraph']


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
    # We're going to use some star magic to chunk the iterable. We create a
    # copy of the iterator size times, then pull a value from each to form a
    # chunk. The last chunk may have some trailing Nones if the length of the
    # iterable isn't a multiple of size, so we filter them out.
    #
    # pylint: disable=star-args
    args = (iter(iterable),) * size

    return (
        itertools.takewhile(lambda x: x is not None, group)
        for group in itertools.zip_longest(*args)
    )


def braillegraph(*args, sep='\n'):
    '''Consume an iterable of integers and produce a bar graph using braille
    characters. If the iterable contains more than four integers, it will be
    chunked into groups of four, separated with newlines by default.

        >>> braillegraph([1, 2, 3, 4])
        '⣷⣄'
        >>> braillegraph([1, 2, 3, 4, 5, 6])
        '⣷⣄\\n⠛⠛⠓'
        >>> print(braillegraph([1, 2, 3, 4, 5, 6]))
        ⣷⣄
        ⠛⠛⠓

    Alternately, the arguments can be passed directly:

        >>> braillegraph(1, 2, 3, 4)
        '⣷⣄'

    The optional sep parameter controls how groups are separated. If sep is not
    passed (or if it is None), they are put on their own lines. For example, to
    keep everything on one line, space could be used:

        >>> braillegraph(3, 1, 4, 1, 5, 9, 2, 6, sep=' ')
        '⡯⠥ ⣿⣛⣓⠒⠂'
    '''
    lines = []

    # If the arguments were passed as a single iterable, pull it out.
    # Otherwise, just use them as-is.
    if len(args) == 1:

        bars = args[0]
    else:
        bars = args

    # Make sure we use the default
    if sep is None:
        sep = '\n'

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
    return sep.join(lines)

