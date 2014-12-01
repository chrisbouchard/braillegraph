braillegraph
============

**A library for creating graphs using Unicode braille characters**

Someone on reddit posted a screenshot of their xmobar setup, which used braille characters to show the loads of their four processor cores, as well as several other metrics. I was impressed that you could fit so much data into a single line. I immediately set out to implement braille bar graphs for myself.

The characters this script outputs are in the Unicode Braille Patterns section, code points 0x2800 through 0x28FF. Not all fonts support these characters, so if you can't see the examples below check your font settings.


Installation
------------
This package is hosted on PyPI, so installation should be as simple as

    % pip install braillegraph

Note that this package requires **at least Python 3.3**, so if your default Python installation is still Python 2, make sure you use `pip3`.

If you want to install from this repository, download it and run

    % python setup.py install

Again, use `python3` if necessary.


Usage
-----

There are two ways to use this package: imported in Python code, or as a command line script.

To use the package in Python, import it and use the `vertical_graph` and `horizontal_graph` functions.

    >>> from braillegraph import vertical_graph, horizontal_graph
    >>> vertical_graph([3, 1, 4, 1])
    '⡯⠥'
    >>> vertical_graph([1, 2, 3, 4, 5, 6])
    '⣷⣄\n⠛⠛⠓'
    >>> print(vertical_graph([1, 2, 3, 4, 5, 6]))
    ⣷⣄
    ⠛⠛⠓
    >>> horizontal_graph([3, 1, 4, 1])
    '⣆⣇'
    >>> horizontal_graph([1, 2, 3, 4, 5, 6])
    '⠀⠀⣠\n⣠⣾⣿'
    >>> print(horizontal_graph([1, 2, 3, 4, 5, 6]))
    ⠀⠀⣠
    ⣠⣾⣿

Alternately, the arguments can be passed directly:

    >>> vertical_graph(3, 1, 4, 1)
    '⡯⠥'
    >>> horizontal_graph(3, 1, 4, 1)
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


Functions
---------

The following functions are defined in the `braillegraph` package. This documentation is also available via the built-in Python `help` function.

###`vertical_graph(*args, sep='\n')`
Consume an iterable of integers and produce a vertical bar graph using braille characters.

The graph is vertical in that its dependent axis is the vertical axis. Thus each value is represented as a row running left to right, and values are listed top to bottom.

If the iterable contains more than four integers, it will be chunked into groups of four, separated with newlines by default.

    >>> vertical_graph([1, 2, 3, 4])
    '⣷⣄'
    >>> vertical_graph([1, 2, 3, 4, 5, 6])
    '⣷⣄\n⠛⠛⠓'
    >>> print(vertical_graph([1, 2, 3, 4, 5, 6]))
    ⣷⣄
    ⠛⠛⠓

Alternately, the arguments can be passed directly:

    >>> vertical_graph(1, 2, 3, 4)
    '⣷⣄'

The optional `sep` parameter controls how groups are separated. If `sep` is not passed (or if it is `None`), they are put on their own lines. For example, to keep everything on one line, space could be used:

    >>> vertical_graph(3, 1, 4, 1, 5, 9, 2, 6, sep=' ')
    '⡯⠥ ⣿⣛⣓⠒⠂'

###`horizontal_graph(*args)`
Consume an iterable of integers and produce a horizontal bar graph using braille characters.

The graph is horizontal in that its dependent axis is the horizontal axis. Thus each value is represented as a column running bottom to top, and values are listed left to right.

The graph is anchored to the bottom, so columns fill in from the bottom of the current braille character and the next character is added on top when needed. For columns with no dots, the blank braille character is used, not a space character.

    >>> horizontal_graph([1, 2, 3, 4])
    '⣠⣾'
    >>> horizontal_graph([1, 2, 3, 4, 5, 6])
    '⠀⠀⣠\n⣠⣾⣿'
    >>> print(horizontal_graph([1, 2, 3, 4, 5, 6]))
    ⠀⠀⣠
    ⣠⣾⣿

Alternately, the arguments can be passed directly:

    >>> horizontal_graph(1, 2, 3, 4)
    '⣠⣾'


License
-------

The code is licensed under the BSD 2-clause license. Please feel free to fork it, mess around with it, or submit issues and pull requests.
