import unittest

import six

import dicttools


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
