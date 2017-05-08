from clevertimapi.session import Session
from clevertimapi.utils import list_wrapper
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class FakeEndpoint(object):
    def __init__(self, key):
        self._key = key

    @property
    def key(self):
        return self._key

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'FakeEndpoint(%s)' % (self._key,)


class TestListWrapperSimple(unittest.TestCase):
    def setUp(self):
        self.session = Session('APIKEY')

        self.lstw = list_wrapper(content=['val1', 'val2', 'val3'])

    def test_simple_append(self):
        self.assertEqual(len(self.lstw), 3)
        self.lstw.append('val4')
        self.assertEqual(list(self.lstw), ['val1', 'val2', 'val3', 'val4'])
        self.assertTrue('val4' in self.lstw)
        self.assertEqual(len(self.lstw), 4)

    def test_simple_extend(self):
        self.lstw.extend(('val4', 'val5'))
        self.lstw.extend(['val6', 'val7'])
        self.assertEqual(list(self.lstw), ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7'])
        self.assertEqual(len(self.lstw), 7)

    def test_simple_insert(self):
        self.lstw.insert(0, 'val0')
        self.lstw.insert(3, 'val33')
        self.assertEqual(list(self.lstw), ['val0', 'val1', 'val2', 'val33', 'val3'])
        self.assertEqual(len(self.lstw), 5)

    def test_simple_remove(self):
        self.lstw.remove('val2')
        self.assertEqual(list(self.lstw), ['val1', 'val3'])

    def test_simple_remove_invalid_value(self):
        with self.assertRaises(ValueError):
            self.lstw.remove('val4')

    def test_simple_pop(self):
        ret = self.lstw.pop(0)
        self.assertEqual(ret, 'val1')
        ret = self.lstw.pop()
        self.assertEqual(ret, 'val3')
        ret = self.lstw.pop()
        self.assertEqual(ret, 'val2')
        with self.assertRaises(IndexError):
            self.lstw.pop()

    def test_simple_clear(self):
        self.lstw.clear()
        self.assertEqual(list(self.lstw), [])


class TestListWrapperEndpoint(unittest.TestCase):

    def setUp(self):
        self.session = Session('APIKEY')

        # self.lstwc = list_wrapper(content=[1, 2, 3], custom_type=FakeEndpoint, session=self.session)

    def Xtest_custom_type_append(self):
        self.assertEqual(len(self.lstwc), 3)
        self.lstw.append(FakeEndpoint(9))
        self.assertEqual(list(self.lstwc), [FakeEndpoint(1), FakeEndpoint(2), FakeEndpoint(3), FakeEndpoint(9)])
        self.assertTrue(FakeEndpoint(2) in self.lstwc)
        self.assertEqual(len(self.lstwc), 4)

    def Xtest_custom_type_extend(self):
        self.lstw.extend(('val4', 'val5'))
        self.lstw.extend(['val6', 'val7'])
        self.assertEqual(list(self.lstw), ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7'])
        self.assertEqual(len(self.lstw), 7)

    def Xtest_custom_type_insert(self):
        self.lstw.insert(0, 'val0')
        self.lstw.insert(3, 'val33')
        self.assertEqual(list(self.lstw), ['val0', 'val1', 'val2', 'val33', 'val3'])
        self.assertEqual(len(self.lstw), 5)

    def Xtest_custom_type_remove(self):
        self.lstw.remove('val2')
        self.assertEqual(list(self.lstw), ['val1', 'val3'])

    def Xtest_custom_type_remove_invalid_value(self):
        with self.assertRaises(ValueError):
            self.lstw.remove('val4')

    def Xtest_custom_type_pop(self):
        ret = self.lstw.pop(0)
        self.assertEqual(ret, 'val1')
        ret = self.lstw.pop()
        self.assertEqual(ret, 'val3')
        ret = self.lstw.pop()
        self.assertEqual(ret, 'val2')
        with self.assertRaises(IndexError):
            self.lstw.pop()

    def Xtest_custom_type_clear(self):
        self.lstw.clear()
        self.assertEqual(list(self.lstw), [])
