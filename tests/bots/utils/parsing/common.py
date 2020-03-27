from unittest import TestCase

import pyparsing

from chatbot.bots.utils.parsing import common


def _test_parser(test_case: TestCase, parser, tests, results, fail_tests):
    for inp, out in zip(tests, results):
        test_case.assertEqual(parser.parseString(inp)[0], out)

    for i in fail_tests:
        test_case.assertRaises(pyparsing.ParseException, parser.parseString, i)


class TestCommon(TestCase):
    def test_update_dict(self):
        dict_list = [{"a": 1}, {"a": 2, "b": 3}, {"b": 4, "c": 0}]

        self.assertEqual(common.update_dict(dict_list), {"a": 2, "b": 4, "c": 0})
        self.assertEqual(common.update_dict(dict_list, int.__add__), {"a": 3, "b": 7, "c": 0})

    def test_int_parser(self):
        tests = ["0", "00000", "-121", "-0"]
        fail_tests = ["a031", "--0231", "0123a"]
        tests_results = [0, 0, -121, 0]

        _test_parser(self, common.common_parsers[int], tests, tests_results, fail_tests)

    def test_str_parser(self):
        tests = ["test", "'test'", "'Hello World'", "\"'Hello World'\"", "Hello World"]
        fail_tests = []
        tests_results = ["test", "test", "Hello World", "'Hello World'", "Hello"]

        _test_parser(self, common.common_parsers[str], tests, tests_results, fail_tests)
