'''Hello'''

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


def chunk(iterable, size):
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

    # Each line can accomodate our bars, one for each row in the braille
    # block.
    for bar_group in chunk(bars, 4):
        line = []

        for braille_row, bar_value in enumerate(bar_group):
            # The number of braille blocks needed to draw this bar
            blocks_needed = (bar_value // 2) + (bar_value % 2)

            # The number of braille blocks we'll need to append to the current
            # line to accomodate this bar
            extra_blocks_needed = blocks_needed - len(line)

            # If we need extra blocks, add them.
            if extra_blocks_needed > 0:
                line.extend([_BRAILLE_EMPTY_BLOCK] * extra_blocks_needed)

            # Fill in the majority of the bar with full braille rows (two dots).
            for block_index in range(bar_value // 2):
                line[block_index] += _BRAILLE_FULL_ROW[braille_row]

            # If the bar's value is odd, we'll need to add a single dot at the
            # end.
            if bar_value % 2:
                block_index = (bar_value // 2)
                line[block_index] += _BRAILLE_HALF_ROW[braille_row]

        # Wrap up this line by converting all the code points to characters
        # and concatenating them.
        lines.append(line)

    # Join all the lines
    return '\n'.join(''.join(chr(code) for code in line) for line in lines)

