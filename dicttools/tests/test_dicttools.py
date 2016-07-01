import unittest

import mock
import six

import dicttools


def is_even(i):
    return i % 2 == 0


class DictToolsTests(unittest.TestCase):
    def test_ByKey_Always_ReturnDictWithValuesAssignedToExtractedKey(self):
        values = (mock.Mock(id=3), mock.Mock(id=6))

        result = dicttools.by('id', values)

        self.assertEqual(values[1], result[6])

    def test_Split_SplitByEvenAndOddKeys_FirstElementShouldContainEvenElements(self):
        elements = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        result = next(dicttools.split(elements, is_even))
        expected = {0: 'A', 2: 'C', 4: 'E'}

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
            value = result['3']

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
        source = {'a': 1, 'b': 2, 'c':4}

        result = dicttools.select(source, 'a', 'c')

        self.assertEqual({'a': 1, 'c':4}, result)


class FrozenDictTests(unittest.TestCase):
    def test_Init_CreateEmptyFrozenDict_LengthIs0(self):
        instance = self.create_frozendict()

        self.assertEqual(0, len(instance))

    def test_Init_CreateFromMapping_LengthIsEqualToMappingLength(self):
        instance = self.create_frozendict({'a': 1, 'b': 2})

        self.assertEqual(2, len(instance))

    def test_Init_CreateFromMapping_SaveContentFromMapping(self):
        instance = self.create_frozendict({'a': 1, 'b': 2})

        self.assertEqual(1, instance['a'])

    def test_Init_CreateFromList_SaveContentFromIterablePairKeyValue(self):
        instance = self.create_frozendict([('pi', 3.14), ('e', 2.72)])

        self.assertEqual(3.14, instance['pi'])

    def test_Init_CreateFromList_LengthIsEqualToMappingLength(self):
        instance = self.create_frozendict([('pi', 3.14), ('e', 2.72)])

        self.assertEqual(2, len(instance))

    def test_Init_CreateFromKwargs_SaveContentFromGivenAssignments(self):
        instance = self.create_frozendict(pi=3.14, e=2.72)

        self.assertEqual(2.72, instance['e'])

    def test_Init_CreateFromKwargsAndFromMapping_SaveContentFromGivenAssignmentsAndMapping(self):
        instance = self.create_frozendict({'pi': 3.14}, e=2.72)

        self.assertEqual(2.72, instance['e'])

    def test_Init_KeyInKwargsAndFromMappingIsRepeated_SaveValueFormKwargs(self):
        instance = self.create_frozendict({'e': 3.14}, e=2.72)

        self.assertEqual(2.72, instance['e'])

    def test_Init_IterableValuesAreNotPairs_Throws(self):
        with self.assertRaisesRegexp(TypeError, "cannot convert dictionary update sequence element #0 to a sequence"):
            self.create_frozendict([1, 2, 3])

    def test_GetItem_NotExists_Throws(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        with self.assertRaisesRegexp(KeyError, 'c'):
            result = instance['c']

    def test_Contains_KeyNotIn_ReturnFalse(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertNotIn('c', instance)

    def test_Contains_KeyIsIn_ReturnTrue(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertIn('b', instance)

    def test_HasKey_KeyNotIn_ReturnFalse(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertFalse(instance.has_key('c'))

    def test_HasKey_KeyIsIn_ReturnTrue(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertTrue(instance.has_key('b'))

    def test_Get_KeyFound_ReturnValueForGivenKey(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertEqual(1, instance.get('b'))

    def test_Get_KeyNotFoundAndDefaultNotGiven_ReturnNone(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertIsNone(instance.get('c'))

    def test_Get_KeyNotFoundAndDefaultWasGiven_ReturnDefault(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertEqual(2.4, instance.get('c', 2.4))

    def test_Items_Always_ReturnListOfKeyValuePaorsAs2Tuples(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        result = instance.items()

        self.assertEqual([('b', 1), ('d', 2)], list(result))

    def test_Values_Always_ReturnListOfValues(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        result = instance.values()

        self.assertEqual([1, 2], list(result))

    def test_Keys_Always_ReturnListOfKeys(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        result = instance.keys()

        self.assertEqual(['b', 'd'], list(result))

    def test_Str_Always_IsDollarAndKeyValuePairsInBraces(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertEqual("${'b': 1, 'd': 2}", str(instance))

    def test_Equal_SameObject_ReturnTrue(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        self.assertEqual(instance, instance)

    def test_Equal_SameContent_ReturnTrue(self):
        a = self.create_frozendict({'b': 1, 'd': 2})
        b = self.create_frozendict({'d': 2, 'b': 1})

        self.assertEqual(a, b)

    def test_Equal_DifferentContent_ReturnFalse(self):
        a = self.create_frozendict({'b': 1, 'd': 2})
        b = self.create_frozendict({'d': 2, 'c': 1})

        self.assertNotEqual(a, b)

    def test_Equal_ToDictWithSameContent_ReturnTrue(self):
        a = self.create_frozendict({'b': 1, 'd': 2})
        b = {'b': 1, 'd': 2}

        self.assertEqual(a, b)

    def test_Iter_Always_IterOverKeys(self):
        instance = self.create_frozendict({'b': 1, 'd': 2})

        result = iter(instance)

        self.assertEqual('b', next(result))
        self.assertEqual('d', next(result))

        with self.assertRaises(StopIteration):
            next(result)

    def test_Hash_ForEqualInstances_AreEqual(self):
        a = self.create_frozendict({'b': 1, 'd': 2})
        b = self.create_frozendict({'d': 2, 'b': 1})

        self.assertEqual(hash(a), hash(b))

    def test_Hash_ForDifferentInstances_AreDifferent(self):
        a = self.create_frozendict({'b': 1, 'd': 2})
        b = self.create_frozendict({'d': 2, 'c': 1})

        self.assertNotEqual(hash(a), hash(b))

    def test_CastToDict_Always_DictContainsAllItemsFromFrozenDict(self):
        frozen = self.create_frozendict({'b': 1, 'd': 2})

        result = dict(frozen)

        self.assertEqual({'b': 1, 'd': 2}, result)

    def test_Copy_Always_ReturnNewObject(self):
        frozen = self.create_frozendict({'b': 1, 'd': 2})

        self.assertIsNot(frozen, frozen.copy())

    def test_Copy_Always_ReturnEqualObject(self):
        frozen = self.create_frozendict({'b': 1, 'd': 2})

        self.assertEqual(frozen, frozen.copy())

    if six.PY2:
        def test_IterItems_Always_ReturnGeneratorOfKeyValuePairsAs2Tuples(self):
            instance = self.create_frozendict({'b': 1, 'd': 2})

            result = instance.iteritems()

            self.assertEqual(('b', 1), next(result))
            self.assertEqual(('d', 2), next(result))

            with self.assertRaises(StopIteration):
                next(result)

        def test_IterValues_Always_ReturnGeneratorOfValues(self):
            instance = self.create_frozendict({'b': 1, 'd': 2})

            result = instance.itervalues()

            self.assertEqual(1, next(result))
            self.assertEqual(2, next(result))

            with self.assertRaises(StopIteration):
                next(result)

        def test_IterKeys_Always_ReturnGeneratorOfKeys(self):
            instance = self.create_frozendict({'b': 1, 'd': 2})

            result = instance.iterkeys()

            self.assertEqual('b', next(result))
            self.assertEqual('d', next(result))

            with self.assertRaises(StopIteration):
                next(result)

    def create_frozendict(self, *args, **kwargs):
        return dicttools.FrozenDict(*args, **kwargs)
