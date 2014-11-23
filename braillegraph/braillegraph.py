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
'''

import itertools


# Only export this function. Everything else is an implementation detail.
__all__ = ['vertical_graph', 'horizontal_graph']


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

# Full columns have all four dots. Partial columns have dots starting from the
# bottom of the block. Note that _BRAILLE_PARTIAL_COL[x][y] represents (y + 1)
# dots.
_BRAILLE_FULL_COL = [0x47, 0xB8]
_BRAILLE_PARTIAL_COL = [
    [0x40, 0x44, 0x46],
    [0x80, 0xA0, 0xB0]
]


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


def _matrix_add_column(matrix, column, default=0):
    '''Given a matrix as a list of lists, add a column to the right, filling in
    with a default value if necessary.
    '''
    extra_rows_needed = len(column) - len(matrix)
    width = len(matrix[0]) if matrix else 0
    offset = 0

    # If we need extra rows, add them to the top of the matrix.
    if extra_rows_needed > 0:
        for _ in range(extra_rows_needed):
            matrix.insert(0, [default] * width)

    # If the column is shorter, we'll need to shift it down.
    if extra_rows_needed < 0:
        offset = -extra_rows_needed
        column = ([default] * offset) + column

    for index, value in enumerate(column):
        matrix[index].append(value)


def vertical_graph(*args, sep='\n'):
    '''Consume an iterable of integers and produce a vertical bar graph using
    braille characters. If the iterable contains more than four integers, it
    will be chunked into groups of four, separated with newlines by default.

        >>> vertical_graph([1, 2, 3, 4])
        '⣷⣄'
        >>> vertical_graph([1, 2, 3, 4, 5, 6])
        '⣷⣄\\n⠛⠛⠓'
        >>> print(vertical_graph([1, 2, 3, 4, 5, 6]))
        ⣷⣄
        ⠛⠛⠓

    Alternately, the arguments can be passed directly:

        >>> vertical_graph(1, 2, 3, 4)
        '⣷⣄'

    The optional sep parameter controls how groups are separated. If sep is not
    passed (or if it is None), they are put on their own lines. For example, to
    keep everything on one line, space could be used:

        >>> vertical_graph(3, 1, 4, 1, 5, 9, 2, 6, sep=' ')
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


def horizontal_graph(*args):
    '''Consume an iterable of integers and produce a horizontal bar graph using
    braille characters.

        >>> horizontal_graph([1, 2, 3, 4])
        '⣠⣾'
        >>> horizontal_graph([1, 2, 3, 4, 5, 6])
        '⠀⠀⣠\\n⣠⣾⣿'
        >>> print(horizontal_graph([1, 2, 3, 4, 5, 6]))
        ⠀⠀⣠
        ⣠⣾⣿

    Alternately, the arguments can be passed directly:

        >>> vertical_graph(1, 2, 3, 4)
        '⣠⣾'
    '''
    lines = []

    # If the arguments were passed as a single iterable, pull it out.
    # Otherwise, just use them as-is.
    if len(args) == 1:

        bars = args[0]
    else:
        bars = args

    # Break the bars into groups of two, one for each column in the braille
    # blocks.
    for bar_group in _chunk(bars, 2):
        column = []

        for braille_col, bar_value in enumerate(bar_group):
            # The number of full braille blocks needed to draw this bar. Each
            # block is four dots tall.
            full_blocks_needed = bar_value // 4

            # The number of braille blocks needed to draw this bar. This
            # accounts for a possible partial block.
            blocks_needed = full_blocks_needed + (1 if bar_value % 4 else 0)

            # The number of new lines we'll need to prepend to accomodate this
            # bar
            extra_blocks_needed = blocks_needed - len(column)

            # If we need extra blocks, add them.
            column = ([_BRAILLE_EMPTY_BLOCK] * extra_blocks_needed) + column

            # Fill in the majority of the column with full braille colums (four
            # dots).
            for block_index in range(-full_blocks_needed, 0, 1):
                column[block_index] += _BRAILLE_FULL_COL[braille_col]

            # If we need a partial column, fill it in.
            if bar_value % 4:
                partial_index = (bar_value % 4) - 1
                column[-blocks_needed] += _BRAILLE_PARTIAL_COL[braille_col][partial_index]

        # Add this column to the lines.
        _matrix_add_column(lines, column, default=_BRAILLE_EMPTY_BLOCK)

    # Convert all the code points into characters, concatenate them into lines,
    # then concatenate all the lines to make the final graph.
    return '\n'.join(''.join(chr(code) for code in line) for line in lines)

