'''Test the braillegraph module.'''

import unittest

from .. import braillegraph

# Don't blame this class for the sins of its father.
# pylint: disable=too-many-public-methods
class HorizontalTestCase(unittest.TestCase):
    '''Test the braillegraph.horizontal_graph function.'''

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

