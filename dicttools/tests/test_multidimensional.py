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

    def test_GetItem_ListInKey_ReturnItemsFromList(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        actual = instance[1, ['A', 'C']]

        self.assertEqual(2, len(actual))
        self.assertEqual(14, actual['C'])

    def test_Contains_KeyInDict_ReturnTrue(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        self.assertIn((1, 'A'), instance)

    def test_Contains_KeyNotInDict_ReturnFalse(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        self.assertNotIn((3, 'A'), instance)

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

    def test_Merge_WithEmptyDict_ReturnNewEqual(self):
        dict1 = self.from_flat({
            (1, 'A'): 12,
            (2, 'B'): 34,
        })

        dict2 = self.create()

        actual = dict1.merge(dict2)

        self.assertIsNot(dict1, actual)
        self.assertEqual(2, len(actual))
        self.assertEqual(34, actual[2, 'B'])

    def test_Merge_NoCommonKeys_ReturnDictWithValuesFromBoth(self):
        dict1 = self.from_flat({
            (1, 'A'): 12,
            (2, 'B'): 34,
        })

        dict2 = self.from_flat({
            (1, 'B'): 13,
            (2, 'A'): 25,
        })

        actual = dict1.merge(dict2)

        self.assertEqual(4, len(actual))
        self.assertEqual(25, actual[2, 'A'])

    def test_Merge_WithCommonKeys_ReturnReplaceValueFromSecondDict(self):
        dict1 = self.from_flat({
            (1, 'A'): 12,
            (1, 'B'): 34,
        })

        dict2 = self.from_flat({
            (1, 'B'): 13,
            (2, 'A'): 25,
        })

        actual = dict1.merge(dict2)

        self.assertEqual(3, len(actual))
        self.assertEqual(13, actual[1, 'B'])

    def test_MapValues_Always_ReturnNewDictWithModifiedValues(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']])

        actual = instance.map_values(lambda v: v % 10)

        self.assertEqual(4, actual[2]['B'])

    create = staticmethod(dicttools.multidimensional.MultiDict)
    from_flat = staticmethod(dicttools.multidimensional.MultiDict.from_flat)


class NamedMultiDictTest(unittest.TestCase):
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

    def test_Reduce_View_ReturnNamedDict(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ], [[1, 2, 3], ['A', 'B']], ['row', 'column'])

        actual = instance.get(column='B').reduce()

        self.assertIsInstance(actual, dicttools.multidimensional.NamedMultiDict)

    def test_Reduce_ListInKey_SustainNamesInResult(self):
        instance = self.create([
            [12, 13],
            [25, 34],
            [56, 89],
        ], [[1, 2, 3], ['A', 'B']], ['row', 'column'])

        reduced = instance.get(row=[1, 3]).reduce()

        actual = reduced.get(row=1, column='B')
        self.assertEqual(13, actual)

    def test_MapValues_Always_ReturnNewDictWithModifiedValues(self):
        instance = self.create([
            [12, 13, 14],
            [25, 34, 35],
        ], headers=[[1, 2], ['A', 'B', 'C']], names=['row', 'column'])

        actual = instance.map_values(lambda v: v % 10)

        self.assertEqual(4, actual.get(row=2, column='B'))

    create = staticmethod(dicttools.multidimensional.NamedMultiDict)
