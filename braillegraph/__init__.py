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

from .braillegraph import vertical_graph, horizontal_graph

__all__ = ['vertical_graph', 'horizontal_graph']

