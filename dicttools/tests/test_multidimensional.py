from __future__ import absolute_import

import unittest
import dicttools.multidimensional


class MultiDictTest(unittest.TestCase):
    def test_GetItem_1Dimension_ReturnAssignedValue(self):
        instance = self.create()

        instance['A'] = 12

        actual = instance['A']

        self.assertEqual(12, actual)

    def test_GetItem_2DimensionGetCell_ReturnAssignedValue(self):
        instance = self.create()

        instance['A', 'C'] = 13

        actual = instance['A', 'C']

        self.assertEqual(13, actual)

    def test_GetItem_GetColumn_ReturnValuesInColumn(self):
        instance = self.create([
            [12, 13],
            [25, 34],
        ], headers=[[1, 2], ['A', 'B']])

        actual = instance[:, 'B']
        expected = [13, 34]

        self.assertEqual(expected, actual)

    @staticmethod
    def create(*args, **kwargs):
        return dicttools.multidimensional.MultiDict(*args, **kwargs)

