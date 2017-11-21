import unittest

from clients.client import downcase, DowncaseError, MetaClient


class TestDowncase(unittest.TestCase):

    def setUp(self):
        @downcase
        def my_function(str):
            return str

        self.my_function = my_function

    def test_lowercases_data(self):
        my_string = 'aBc 1234 $@!#'
        output = self.my_function(my_string)

        self.assertEqual(output, my_string.lower())

        my_object = {'Abc': 123, '123': 'aBC'}
        output = self.my_function(my_object)

        self.assertDictEqual(output, {'abc': 123, '123': 'abc'})

    def test_failure_raises_error(self):
        not_downcaseable = lambda x: x

        with self.assertRaises(DowncaseError):
            self.my_function(not_downcaseable)


class TestDowncase(unittest.TestCase):

    def setUp(self):
        @downcase
        def my_function(str):
            return str

        self.my_function = my_function

    def test_lowercases_data(self):
        my_string = 'aBc 1234 $@!#'
        output = self.my_function(my_string)

        self.assertEqual(output, my_string.lower())

        my_object = {'Abc': 123, '123': 'aBC'}
        output = self.my_function(my_object)

        self.assertDictEqual(output, {'abc': 123, '123': 'abc'})

    def test_failure_raises_error(self):
        not_downcaseable = lambda x: x

        with self.assertRaises(DowncaseError):
            self.my_function(not_downcaseable)


class TestMetaClient(unittest.TestCase):

    def setUp(self):
        self.kwargs = {'liqui': {}, 'poloniex': {}}

    def test_init(self):
        client = MetaClient(**self.kwargs)
        self.assertEqual(len(client.helpers), 2)

    def test_init_unsupported_exchange(self):
        self.kwargs['unsupported'] = {}

        with self.assertRaisesRegexp(NotImplementedError, 'unsupported is not implemented!'):
            MetaClient(**self.kwargs)