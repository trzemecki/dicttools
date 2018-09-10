from __future__ import absolute_import

import unittest

try:
    import mock
except ImportError:
    from unittest import mock

import dicttools
import collections


def is_even(i):
    return i % 2 == 0


class DictToolsTests(unittest.TestCase):
    def test_Merge_3DictsGiven_ReturnDictContainingEachElementFromGivenDicts(self):
        result = dicttools.merge({'A': 1}, {'B': 2}, {'C': 3})

        expected = {'A': 1, 'B': 2, 'C': 3}
        self.assertEqual(expected, result)

    def test_Merge_ByDefault_ReturnEmptyDict(self):
        result = dicttools.merge()

        self.assertEqual({}, result)

    def test_Merge_KeyRepeats_ReturnDictWithValueFromLast(self):
        result = dicttools.merge({'A': 1, 'X': 8}, {'B': 2, 'X': 14}, {'C': 3, 'X': 12})

        self.assertEqual(12, result['X'])

    def test_Merge_KeyRepeats_MergeFuncIsSum_ReturnDictWithAddedDuplicatedValues(self):
        result = dicttools.merge(lambda x, y: x + y, {'A': 1, 'X': 8}, {'B': 2, 'X': 14}, {'C': 3, 'X': 12})

        self.assertEqual(34, result['X'])

    def test_Merge_KeyRepeats_MergeFuncIsDifference_ReturnDictWithValuesSubtractedValues(self):
        result = dicttools.merge(lambda x, y: x - y, {'A': 1, 'X': 8}, {'B': 2, 'X': 14}, {'C': 3, 'X': 12})

        self.assertEqual(-18, result['X'])

    def test_Merge_NoneGivenAsThridArgument_IgnoreNones(self):
        result = dicttools.merge({'A': 1}, {'B': 2}, None, {'C': 3})

        self.assertEqual({'A', 'B', 'C'}, set(result))

    def test_Merge_NoneGivenAsFirstArgument_IgnoreNones(self):
        result = dicttools.merge(None, {'A': 1}, {'B': 2}, {'C': 3})

        self.assertEqual({'A', 'B', 'C'}, set(result))

    def test_Merge_NoneGiven_MergeFuncGivenAndThirdArgumentIsNone_IgnoreNones(self):
        result = dicttools.merge(lambda x, y: x + y, {'A': 1}, {'B': 2}, None, {'C': 3})

        self.assertEqual({'A', 'B', 'C'}, set(result))

    def test_Merge_NoneGiven_MergeFuncGivenAndFirstArgumentIsNone_IgnoreNones(self):
        result = dicttools.merge(lambda x, y: x + y, None, {'A': 1}, {'B': 2}, {'C': 3})

        self.assertEqual({'A', 'B', 'C'}, set(result))

    def test_Merge_OnlyNonesGiven_ReturnEmptyDict(self):
        result = dicttools.merge(None, None)

        self.assertEqual({}, result)

    def test_Merge_NestedDicts(self):
        mydicts = [{"a": {"x": 1, "y": 2}, "b": {"x": 1, "z": 3}}, {"a": {"x": 1, "y": 5}, "c": {"x": 1, "z": 3}}]

        actual = dicttools.merge(lambda d1, d2: dicttools.merge(lambda x, y: x + y, d1, d2), *mydicts)
        expected = {"a": {"x": 2, "y": 7}, "b": {"x": 1, "z": 3}, "c": {"x": 1, "z": 3}}

        self.assertEqual(expected, actual)

    def test_Merge_OrderedDicts_ReturnOrderedDict(self):
        dict1 = collections.OrderedDict((('a', 1), ('b', 2)))
        dict2 = collections.OrderedDict((('b', 1), ('c', 2)))

        actual = dicttools.merge(dict1, dict2)
        expected = collections.OrderedDict((('a', 1), ('b', 1), ('c', 2)))

        self.assertIsInstance(actual, collections.OrderedDict)
        self.assertEqual(expected, actual)

    def test_ByKey_Always_ReturnDictWithValuesAssignedToExtractedKey(self):
        values = (mock.Mock(id=3), mock.Mock(id=6))

        result = dicttools.by('id', values)

        self.assertEqual(values[1], result[6])

    def test_Split_SplitByEvenAndOddKeys_FirstElementShouldContainEvenElements(self):
        elements = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        result = next(dicttools.split(elements, is_even))
        expected = {0: 'A', 2: 'C', 4: 'E'}

        self.assertEqual(expected, result)

    def test_Split_SplitByValues_GiveValueToCondition(self):
        elements = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}

        result, = dicttools.split(elements, lambda val: val % 2 == 0, rest=False)
        expected = {'A': 0, 'C': 2, 'E': 4}

        self.assertEqual(expected, result)

    def test_Sift_SiftEventKey_ResultShouldContainOnlyEvenElements(self):
        elements = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        result = dicttools.sift(elements, is_even)

        expected = {0: 'A', 2: 'C', 4: 'E'}
        self.assertEqual(expected, result)

    def test_Sift_SiftNotNoneValues_ResultShouldContainElementsWithNotNoneValues(self):
        elements = {0: None, 1: 'B', 2: None, 3: 'D', 4: 'E'}

        result = dicttools.sift(elements, lambda k, v: v is not None)

        expected = {1: 'B', 3: 'D', 4: 'E'}
        self.assertEqual(expected, result)

    def test_SiftUpdate_SiftEventKey_ResultShouldContainOnlyEvenElements(self):
        elements = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        dicttools.sift_update(elements, is_even)

        expected = {0: 'A', 2: 'C', 4: 'E'}
        self.assertEqual(expected, elements)

    def test_SiftUpdate_SiftNotNoneValues_ResultShouldContainElementsWithNotNoneValues(self):
        elements = {0: None, 1: 'B', 2: None, 3: 'D', 4: 'E'}

        dicttools.sift_update(elements, lambda k, v: v is not None)

        expected = {1: 'B', 3: 'D', 4: 'E'}
        self.assertEqual(expected, elements)

    def test_Split_SplitByNoneOrNoneValues_ResultShouldContainElementsWithNotNoneValues(self):
        elements = {0: None, 1: 'B', 2: None, 3: 'D', 4: 'E'}

        result = next(dicttools.split(elements, lambda k, v: v is not None))
        expected = {1: 'B', 3: 'D', 4: 'E'}

        self.assertEqual(expected, result)

    def test_Contains_EmptyDict_ReturnTrue(self):
        elements = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        result = dicttools.contains(sub={}, super=elements)

        self.assertTrue(result)

    def test_Contains_SelfContaining_ReturnTrue(self):
        elements = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        result = dicttools.contains(sub=elements, super=elements)

        self.assertTrue(result)

    def test_Contains_NotEmptyInEmpty_ReturnFalse(self):
        elements = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        result = dicttools.contains(sub=elements, super={})

        self.assertFalse(result)

    def test_Contains_EmptyInEmpty_ReturnTrue(self):
        result = dicttools.contains({}, {})

        self.assertTrue(result)

    def test_Contains_DictWithAdditionalElements_ReturnFalse(self):
        sup = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        sub = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}

        result = dicttools.contains(sub, sup)

        self.assertFalse(result)

    def test_Contains_ValueMismatch_ReturnFalse(self):
        sup = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        sub = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'F'}

        result = dicttools.contains(sub, sup)

        self.assertFalse(result)

    def test_Swap_Always_ReplacedValuesWithKeys(self):
        elements = {0: 'A', 1: 'B', 2: 'C'}

        result = dicttools.swap(elements)

        self.assertEqual({'A': 0, 'B': 1, 'C': 2}, result)

    def test_TwoWay_Always_CreatedNewDictWithGivenValuesAndSwapped(self):
        elements = {0: 'A', 1: 'B', 2: 'C'}

        result = dicttools.two_way(elements)

        self.assertEqual({0: 'A', 1: 'B', 2: 'C', 'A': 0, 'B': 1, 'C': 2}, result)

    def test_GroupBy_Always_ReturnDictOfListElementGroupedByGivenAttribute(self):
        values = (mock.Mock(id=3, sort='1'), mock.Mock(id=6, sort='2'), mock.Mock(id=4, sort='1'))

        result = dicttools.group_by('sort', values)

        self.assertEqual({values[0], values[2]}, set(result['1']))

    def test_GroupBy_TryTakeNotContainedKey_Throws(self):
        values = (mock.Mock(id=3, sort='1'), mock.Mock(id=6, sort='2'), mock.Mock(id=4, sort='1'))

        result = dicttools.group_by('sort', values)

        with self.assertRaises(KeyError):
            _ = result['3']

    def test_Extract_KeyNotGiven_ReturnDictWithAttributes(self):
        source = mock.Mock(first=1, second=2, third=3)

        result = dicttools.extract(source, 'first', 'second')

        self.assertEqual({'first': 1, 'second': 2}, result)

    def test_Extract_KeyGiven_UseKeyToExtract(self):
        def caesar(source, item):
            return getattr(source, chr(ord(item) + 1))

        result = dicttools.extract(mock.Mock(i=2, b=3, m=4), 'h', 'a', 'l', key=caesar)

        self.assertEqual({'h': 2, 'a': 3, 'l': 4}, result)

    def test_Select_Always_GetFromDictGivenItems(self):
        source = {'a': 1, 'b': 2, 'c': 4}

        result = dicttools.select(source, 'a', 'c')

        self.assertEqual({'a': 1, 'c': 4}, result)

    def test_MapValues_Always_ReturnValuesWithTheSameKeysAndMappedValues(self):
        source = {'a': 1, 'b': 2, 'c': 4}

        result = dicttools.map_values(lambda v: v + 1, source)

        self.assertEqual({'a': 2, 'b': 3, 'c': 5}, result)

    def test_MapKeys_Always_ReturnValuesWithMappedKeysAndTheSameValues(self):
        source = {'h': 1, 'a': 2, 'l': 3}

        result = dicttools.map_keys(lambda v: chr(ord(v) + 1), source)

        self.assertEqual({'i': 1, 'b': 2, 'm': 3}, result)

    def test_FindKey_ValueNotInDict_ReturnDefaultValue(self):
        elements = {'h': 1, 'a': 2, 'l': 3}

        result = dicttools.find_key(4, elements, default='y')

        self.assertEqual('y', result)

    def test_FindKey_ValueUniqueInDict_ReturnKeyForGivenValue(self):
        elements = {'h': 1, 'a': 2, 'l': 3}

        result = dicttools.find_key(2, elements, default='y')

        self.assertEqual('a', result)

    def test_FindKey_ValueDuplicatedInDict_ReturnAnyKeyForGivenValue(self):
        elements = {'h': 1, 'a': 2, 'l': 3, 'x': 1}

        result = dicttools.find_key(1, elements, default='y')

        self.assertEqual(1, elements[result])

    def test_FillValue_NoKeys_ReturnEmptyDict(self):
        actual = dicttools.fill_value([], 'val')

        self.assertEqual({}, actual)

    def test_FillValue_ListOfKeysGiven_ReturnDictWithAssignedValueForEachGivenKey(self):
        keys = ['alpha', 'beta', 'gamma']

        actual = dicttools.fill_value(keys, 'val')

        expected = {
            'alpha': 'val', 'beta': 'val', 'gamma': 'val'
        }
        self.assertEqual(expected, actual)

    def test_Stringify_SingleLevelDict_ReturnSortedKeysWithValues(self):
        d = {"a": 1, "c": 3, "b": 2}
        actual = dicttools.stringify(d)
        expected = "{a:1, b:2, c:3}"
        self.assertEqual(expected, actual)

    def test_Stringify_DoubleNestedDict_CallRecursive(self):
        d = {"a": 1, "c": 3, "b": {"d": 4, "a": 5}}
        actual = dicttools.stringify(d)
        expected = "{a:1, b:{a:5, d:4}, c:3}"

        self.assertEqual(expected, actual)

    def test_ListOfValues_WithoutDefault_ReturnNoneForMissedValues(self):
        actual = dicttools.list_of_values({"a": 1, "b": 2, "d": 4}, ["d", "c", "b", "a"])
        expected = [4, None, 2, 1]

        self.assertEqual(expected, actual)

    def test_ListOfValues_DefaultGiven_ReturnDefaultValueForMissedValues(self):
        actual = dicttools.list_of_values({"a": 1, "b": 2, "d": 4}, ["d", "c", "b", "a"], default=0)
        expected = [4, 0, 2, 1]

        self.assertEqual(expected, actual)
