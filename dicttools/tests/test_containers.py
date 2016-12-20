from __future__ import absolute_import

import unittest

import six

import dicttools


class FrozenDictTests(unittest.TestCase):
    def test_Init_CreateEmptyFrozenDict_LengthIs0(self):
        instance = self.create()

        self.assertEqual(0, len(instance))

    def test_Init_CreateFromMapping_LengthIsEqualToMappingLength(self):
        instance = self.create({'a': 1, 'b': 2})

        self.assertEqual(2, len(instance))

    def test_Init_CreateFromMapping_SaveContentFromMapping(self):
        instance = self.create({'a': 1, 'b': 2})

        self.assertEqual(1, instance['a'])

    def test_Init_CreateFromList_SaveContentFromIterablePairKeyValue(self):
        instance = self.create([('pi', 3.14), ('e', 2.72)])

        self.assertEqual(3.14, instance['pi'])

    def test_Init_CreateFromList_LengthIsEqualToMappingLength(self):
        instance = self.create([('pi', 3.14), ('e', 2.72)])

        self.assertEqual(2, len(instance))

    def test_Init_CreateFromKwargs_SaveContentFromGivenAssignments(self):
        instance = self.create(pi=3.14, e=2.72)

        self.assertEqual(2.72, instance['e'])

    def test_Init_CreateFromKwargsAndFromMapping_SaveContentFromGivenAssignmentsAndMapping(self):
        instance = self.create({'pi': 3.14}, e=2.72)

        self.assertEqual(2.72, instance['e'])

    def test_Init_KeyInKwargsAndFromMappingIsRepeated_SaveValueFormKwargs(self):
        instance = self.create({'e': 3.14}, e=2.72)

        self.assertEqual(2.72, instance['e'])

    def test_Init_IterableValuesAreNotPairs_Throws(self):
        with self.assertRaisesRegexp(TypeError, "'int' object is not iterable"):
            self.create([1, 2, 3])

    def test_GetItem_NotExists_Throws(self):
        instance = self.create({'b': 1, 'd': 2})

        with self.assertRaisesRegexp(KeyError, 'c'):
            result = instance['c']

    def test_Contains_KeyNotIn_ReturnFalse(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertNotIn('c', instance)

    def test_Contains_KeyIsIn_ReturnTrue(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertIn('b', instance)

    def test_HasKey_KeyNotIn_ReturnFalse(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertFalse(instance.has_key('c'))

    def test_HasKey_KeyIsIn_ReturnTrue(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertTrue(instance.has_key('b'))

    def test_Get_KeyFound_ReturnValueForGivenKey(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertEqual(1, instance.get('b'))

    def test_Get_KeyNotFoundAndDefaultNotGiven_ReturnNone(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertIsNone(instance.get('c'))

    def test_Get_KeyNotFoundAndDefaultWasGiven_ReturnDefault(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertEqual(2.4, instance.get('c', 2.4))

    def test_Items_Always_ReturnListOfKeyValuePaorsAs2Tuples(self):
        instance = self.create({'b': 1, 'd': 2})

        result = instance.items()

        self.assertEqual([('b', 1), ('d', 2)], list(result))

    def test_Values_Always_ReturnListOfValues(self):
        instance = self.create({'b': 1, 'd': 2})

        result = instance.values()

        self.assertEqual([1, 2], list(result))

    def test_Keys_Always_ReturnListOfKeys(self):
        instance = self.create({'b': 1, 'd': 2})

        result = instance.keys()

        self.assertEqual(['b', 'd'], list(result))

    def test_Keys_InitWitKeysInOrder_KeepKeysInGivenOrder(self):
        instance = self.create([('d', 1), ('b', 2), ('c', 3)])

        result = instance.keys()

        self.assertEqual(['d', 'b', 'c'], list(result))

    def test_Str_Always_IsDollarAndKeyValuePairsInBraces(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertEqual("${'b': 1, 'd': 2}", str(instance))

    def test_Equal_SameObject_ReturnTrue(self):
        instance = self.create({'b': 1, 'd': 2})

        self.assertEqual(instance, instance)

    def test_Equal_SameContent_ReturnTrue(self):
        a = self.create({'b': 1, 'd': 2})
        b = self.create({'d': 2, 'b': 1})

        self.assertEqual(a, b)

    def test_Equal_DifferentContent_ReturnFalse(self):
        a = self.create({'b': 1, 'd': 2})
        b = self.create({'d': 2, 'c': 1})

        self.assertNotEqual(a, b)

    def test_Equal_ToDictWithSameContent_ReturnTrue(self):
        a = self.create({'b': 1, 'd': 2})
        b = {'b': 1, 'd': 2}

        self.assertEqual(a, b)

    def test_Iter_Always_IterOverKeys(self):
        instance = self.create({'b': 1, 'd': 2})

        result = iter(instance)

        self.assertEqual('b', next(result))
        self.assertEqual('d', next(result))

        with self.assertRaises(StopIteration):
            next(result)

    def test_Hash_ForEqualInstances_AreEqual(self):
        a = self.create({'b': 1, 'd': 2})
        b = self.create({'d': 2, 'b': 1})

        self.assertEqual(hash(a), hash(b))

    def test_Hash_ForDifferentInstances_AreDifferent(self):
        a = self.create({'b': 1, 'd': 2})
        b = self.create({'d': 2, 'c': 1})

        self.assertNotEqual(hash(a), hash(b))

    def test_CastToDict_Always_DictContainsAllItemsFromFrozenDict(self):
        frozen = self.create({'b': 1, 'd': 2})

        result = dict(frozen)

        self.assertEqual({'b': 1, 'd': 2}, result)

    def test_Copy_Always_ReturnNewObject(self):
        frozen = self.create({'b': 1, 'd': 2})

        self.assertIsNot(frozen, frozen.copy())

    def test_Copy_Always_ReturnEqualObject(self):
        frozen = self.create({'b': 1, 'd': 2})

        self.assertEqual(frozen, frozen.copy())

    if six.PY2:
        def test_IterItems_Always_ReturnGeneratorOfKeyValuePairsAs2Tuples(self):
            instance = self.create({'b': 1, 'd': 2})

            result = instance.iteritems()

            self.assertEqual(('b', 1), next(result))
            self.assertEqual(('d', 2), next(result))

            with self.assertRaises(StopIteration):
                next(result)

        def test_IterValues_Always_ReturnGeneratorOfValues(self):
            instance = self.create({'b': 1, 'd': 2})

            result = instance.itervalues()

            self.assertEqual(1, next(result))
            self.assertEqual(2, next(result))

            with self.assertRaises(StopIteration):
                next(result)

        def test_IterKeys_Always_ReturnGeneratorOfKeys(self):
            instance = self.create({'b': 1, 'd': 2})

            result = instance.iterkeys()

            self.assertEqual('b', next(result))
            self.assertEqual('d', next(result))

            with self.assertRaises(StopIteration):
                next(result)

    @staticmethod
    def create(*args, **kwargs):
        return dicttools.FrozenDict(*args, **kwargs)


class ChainMapTest(unittest.TestCase):
    def test_GetItem_ItemInLastDict_ReturnValue(self):
        chain = self.create([
            {'a': 1, 'b': 2},
            {'c': 3, 'd': 4},
            {'e': 5, 'f': 6},
        ])
        
        self.assertEqual(6, chain['f'])

    def test_GetItem_ItemInFirstAndLastDict_ReturnValueFromFirst(self):
        chain = self.create([
            {'a': 1, 'b': 2},
            {'c': 3, 'd': 4},
            {'e': 5, 'a': 6},
        ])

        self.assertEqual(1, chain['a'])

    def test_GetItem_ItemNotInChain_Throws(self):
        chain = self.create([
            {'a': 1, 'b': 2},
            {'c': 3, 'd': 4},
            {'e': 5, 'f': 6},
        ])

        with self.assertRaisesRegexp(KeyError, 'g'):
            r = chain['g']

    def test_Get_ItemInChain_ReturnValue(self):
        chain = self.create([
            {'a': 1, 'b': 2},
            {'c': 3, 'd': 4},
            {'e': 5, 'f': 6},
        ])

        self.assertEqual(4, chain.get('d', -1))

    def test_Get_ItemNotInChain_ReturnValue(self):
        chain = self.create([
            {'a': 1, 'b': 2},
            {'c': 3, 'd': 4},
            {'e': 5, 'f': 6},
        ])

        self.assertEqual(-1, chain.get('x', -1))

    def test_SetItem_ItemInOneMap_ChangeValueInMap(self):
        chain = self.create([
            {'a': 1, 'b': 2},
            {'c': 3, 'd': 4},
            {'e': 5, 'f': 6},
        ])

        chain['d'] = 98

        self.assertEqual(98, chain['d'])

    def test_SetItem_ItemInManyMaps_ChangeValueInFirstFoundedMap(self):
        maps = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'a': 6}]
        chain = self.create(maps)

        chain['a'] = 98

        self.assertEqual(98, maps[0]['a'])
        self.assertEqual(6, maps[-1]['a'])

    def test_SetItem_ItemNotInChain_Throws(self):
        maps = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'a': 6}]
        chain = self.create(maps)

        with self.assertRaisesRegexp(KeyError, 'x'):
            chain['x'] = 98

    def test_DelItem_ItemInManyMaps_DeleteFirstFoundedItem(self):
        maps = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'a': 6}]
        chain = self.create(maps)

        del chain['a']

        self.assertEqual(6, chain['a'])

    def test_DelItem_ItemNotInChain_Throws(self):
        maps = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'a': 6}]
        chain = self.create(maps)

        with self.assertRaisesRegexp(KeyError, 'x'):
            del chain['x']

    def test_Len_Always_ReturnSumOfLengthOfMaps(self):
        maps = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'a': 6}]
        chain = self.create(maps)
        
        self.assertEqual(6, len(chain))
        
    def test_Iter_Always_ReturnKeysGenerator(self):
        maps = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'a': 6}]
        chain = self.create(maps)

        result = sorted(chain)

        self.assertEqual(['a', 'a', 'b', 'c', 'd', 'e'], result)

    @staticmethod
    def create(maps):
        return dicttools.ChainMap(maps)


class TwoWayDictTest(unittest.TestCase):
    def test_Init_GiveDictWith2UniqueValues_Contains4Elements(self):
        container = self.create({'alpha': 'beta', 'gamma': 'delta'})

        self.assertEqual(4, len(container))

    def test_Init_GiveDictWith1EqualKeyAndValue_Contains1Elements(self):
        container = self.create({'alpha': 'alpha'})

        self.assertEqual(1, len(container))

    def test_Init_GiveDictWithPairAndReversedPair_Contains2Elements(self):
        container = self.create({'alpha': 'beta', 'beta': 'alpha'})

        self.assertEqual(2, len(container))

    def test_Init_GiveDictWithNotHashableValue_Throws(self):
        with self.assertRaisesRegexp(TypeError, "unhashable type: 'list'"):
            container = self.create({'alpha': ['beta']})

    def test_SetItem_GetByKey_ReturnValue(self):
        container = self.create()

        container['alpha'] = 'omega'

        self.assertEqual('omega', container['alpha'])

    def test_SetItem_GetByValue_ReturnKey(self):
        container = self.create()

        container['alpha'] = 'omega'

        self.assertEqual('alpha', container['omega'])

    def test_GetItem_ItemNotFound_Throws(self):
        container = self.create()

        container['alpha'] = 'omega'

        with self.assertRaises(KeyError):
            value = container['delta']

    def test_Len_2ElementsAssigned_Return4(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['delta'] = 'beta'

        result = len(container)

        self.assertEqual(4, result)

    def test_SetItem_ReassignExistedKey_RemovePreviousValue(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['alpha'] = 'beta'

        with self.assertRaises(KeyError):
            value = container['omega']

    def test_SetItem_ReassignExistedValue_RemovePreviousKey(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['delta'] = 'omega'

        with self.assertRaises(KeyError):
            value = container['alpha']

    def test_SetItem_ReassignTheSameValue_Contains2Values(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['alpha'] = 'omega'

        self.assertEqual(2, len(container))

    def test_SetItem_ReassignReversed_Contains2Values(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['omega'] = 'alpha'

        self.assertEqual(2, len(container))

    def test_SetItem_AssignNotHashableElement_DoNotModify(self):
        container = self.create()

        container['alpha'] = 'omega'

        with self.assertRaisesRegexp(TypeError, "unhashable type: 'list'"):
            container['delta'] = ['beta']

        self.assertEqual(2, len(container))

    def test_Iter_Always_IterByBothKeyAndValues(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['delta'] = 'beta'

        result = set(iter(container))

        self.assertEqual({'alpha', 'beta', 'delta', 'omega'}, result)

    def test_SetItem_ReassignEqualKeyAndValue_Contains1Values(self):
        container = self.create()

        container['alpha'] = 'alpha'
        container['alpha'] = 'alpha'

        self.assertEqual(1, len(container))

    def test_DelItem_DeleteKey_RemoveKeyAndValue(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['delta'] = 'beta'

        del container['delta']

        result = set(iter(container))
        self.assertEqual({'alpha', 'omega'}, result)

    def test_DelItem_DeleteValue_RemoveKeyAndValue(self):
        container = self.create()

        container['alpha'] = 'omega'
        container['delta'] = 'beta'

        del container['beta']

        result = set(iter(container))
        self.assertEqual({'alpha', 'omega'}, result)

    def test_DelItem_SameKeyAndValue_RemoveBoth(self):
        container = self.create()

        container['alpha'] = 'alpha'
        container['delta'] = 'beta'

        del container['alpha']

        result = set(iter(container))
        self.assertEqual({'delta', 'beta'}, result)

    def test_Str_OnePair_ReturnStringWithKeyValuesPairsAsSimpleDict(self):
        container = self.create()

        container['delta'] = 'beta'

        self.assertEqual("{'delta': 'beta', 'beta': 'delta'}", str(container))

    def test_Str_EqualKeyAndValue_Return1Value(self):
        container = self.create()

        container['alpha'] = 'alpha'

        self.assertEqual("{'alpha': 'alpha'}", str(container))

    def test_Repr_Always_ReturnStringWithOnlyDirectAssignment(self):
        container = self.create()

        container['delta'] = 'beta'

        self.assertEqual("TwoWayDict({'delta': 'beta'})", repr(container))



    @staticmethod
    def create(*args, **kwargs):
        return dicttools.TwoWayDict(*args, **kwargs)
