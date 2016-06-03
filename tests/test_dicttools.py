import unittest
import dicttools
import mock


def is_even(i):
    return i % 2 == 0


class DictToolsTest(unittest.TestCase):
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
            result['3']

