'''Test the braillegraph module.'''

import unittest

from .. import braillegraph

class HorizontalGraphTestCase(unittest.TestCase):
    '''Test the braillegraph.horizontal_graph function.'''

    # Don't blame this class for the sins of its father.
    # pylint: disable=too-many-public-methods

    def test_one_line_range(self):
        '''Test a range of four numbers that fits one one line.'''
        self.assertEqual(
            braillegraph.horizontal_graph(range(1, 5)),
            '⣠⣾'
        )

    def test_two_line_range(self):
        '''Test a range of four numbers that requires two lines.'''
        self.assertEqual(
            braillegraph.horizontal_graph(range(1, 7)),
            '⠀⠀⣠\n⣠⣾⣿'
        )

    def test_multi_args(self):
        '''Test passing multiple arguments.'''
        self.assertEqual(
            braillegraph.horizontal_graph(3, 1, 4, 1, 5, 9, 2, 6),
            '⠀⠀⢀\n⠀⠀⣸⢠\n⣆⣇⣿⣼'
        )

    def test_negative(self):
        '''Test passing negative arguments.'''
        self.assertEqual(
            braillegraph.horizontal_graph(4, 3, 2, 1, -1, -2, -3, -4),
            '⣷⣄⠀⠀\n⠀⠀⠙⢿'
        )


class VerticalGraphTestCase(unittest.TestCase):
    '''Test the braillegraph.vertical_graph function.'''

    # Don't blame this class for the sins of its father.
    # pylint: disable=too-many-public-methods

    def test_one_line_range(self):
        '''Test a range of four numbers that fits one one line.'''
        self.assertEqual(
            braillegraph.vertical_graph(range(1, 5)),
            '⣷⣄'
        )

    def test_two_line_range(self):
        '''Test a range of four numbers that requires two lines.'''
        self.assertEqual(
            braillegraph.vertical_graph(range(1, 7)),
            '⣷⣄\n⠛⠛⠓'
        )

    def test_multi_args(self):
        '''Test passing multiple arguments.'''
        self.assertEqual(
            braillegraph.vertical_graph(3, 1, 4, 1, 5, 9, 2, 6),
            '⡯⠥\n⣿⣛⣓⠒⠂'
        )

