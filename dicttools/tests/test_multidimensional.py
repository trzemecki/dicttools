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

    def test_GetItem_ByCascade_ReturnValue(self):
        instance = self.create([
            [12, 13],
            [25, 34],
        ], headers=[[1, 2], ['A', 'B']])

        actual = instance[1]['B']

        self.assertEqual(13, actual)

    def test_GetItem_KeyNotInView_Throws(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        view = instance[1, 'A':'B']

        with self.assertRaises(KeyError):
            actual = view['C']

    def test_Shape_DictHasValues_ReturnTupleWithDimensions(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ])

        actual = instance.shape

        self.assertEqual((3, 2), actual)

    def test_Shape_DictNotInit_ReturnEmptyTuple(self):
        instance = self.create()

        actual = instance.shape

        self.assertEqual((), actual)

    def test_Size_DictHasValues_ReturnNumberOfDimensions(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ])

        actual = instance.size

        self.assertEqual(2, actual)

    def test_Size_DictNotInit_Return0(self):
        instance = self.create()

        actual = instance.size

        self.assertEqual(0, actual)

    def test_SetItem_ByTuple_ReplaceValueWithGiven(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ])

        instance[1, 1] = 65

        expected = [
            [12, 13],
            [25, 65],
            [56, 89],
        ]

        self.assertEqual(expected, instance)

    def test_SetItem_InView_ReplaceValueWithGiven(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ])

        instance[1][1] = 65

        expected = [
            [12, 13],
            [25, 65],
            [56, 89],
        ]

        self.assertEqual(expected, instance)

    @staticmethod
    def create(*args, **kwargs):
        return dicttools.multidimensional.MultiDict(*args, **kwargs)

