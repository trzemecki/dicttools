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

    def test_Items_2Dimensional_ReturnAllSetItems(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        items = instance.items()

        self.assertEqual(6, len(items))

    def test_Items_2Dimensional_ReturnKeyWithValue(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        items = instance.items()

        self.assertIn(((1, 'B'), 13), items)

    def test_ToNested_2Dimensional_RowDictsNestedInDict(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        actual = instance.to_nested()

        self.assertIsInstance(actual, dict)
        self.assertEqual(34, actual[2]['B'])

    def test_FromFlat_ItemsGiven_ReturnMultiDictWithGivenValues(self):
        instance = self.from_flat({
            (1, 'A'): 12,
            (2, 'B'): 34,
        })

        actual = instance[2, 'B']

        self.assertEqual(34, actual)

    create = staticmethod(dicttools.multidimensional.MultiDict)
    from_flat = staticmethod(dicttools.multidimensional.MultiDict.from_flat)


class NamedMultiDict(unittest.TestCase):
    def test_Get_GiveAllKeys_ReturnAssignedValue(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ], [[1, 2, 3], ['A', 'B']], ['row', 'column'])

        actual = instance.get(row=2, column='B')

        self.assertEqual(34, actual)

    def test_Get_GetValuePartial_ReturnAssignedValue(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ], [[1, 2, 3], ['A', 'B']], ['row', 'column'])

        actual = instance.get(row=2).get(column='B')

        self.assertEqual(34, actual)

    def test_Get_GetValuePartialStartInNested_ReturnAssignedValue(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ], [[1, 2, 3], ['A', 'B']], ['row', 'column'])

        actual = instance.get(column='B').get(row=2)

        self.assertEqual(34, actual)

    @staticmethod
    def create(*args, **kwargs):
        return dicttools.multidimensional.NamedMultiDict(*args, **kwargs)
