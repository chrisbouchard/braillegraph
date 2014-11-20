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

To use the package in Python, import it and use the `braillegraph` function.

    >>> from braillegraph import braillegraph
    >>> braillegraph([1, 2, 3, 4])
    '⣷⣄'

The function takes an iterable of integers, and returns a string. If the iterable contains more than four integers, it will be chunked into groups of four, separated with newlines.

    >>> braillegraph([1, 2, 3, 4, 5, 6])
    '⣷⣄\n⠛⠛⠓'
    >>> print(braillegraph([1, 2, 3, 4, 5, 6]))
    ⣷⣄
    ⠛⠛⠓

To use the package as a script, run it as

    % python -m braillegraph 1 2 3 4 5 6
    ⣷⣄
    ⠛⠛⠓
    
For a description of the arguments and flags, run

    % python -m braillegraph --help
    
License
-------

The code is licensed under the BSD 2-clause license. Please feel free to fork it, mess around with it, or submit issues and pull requests.
