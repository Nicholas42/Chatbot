from unittest import TestCase

from chatbot.bots.utils.parsing import common


class TestCommon(TestCase):
    def test_update_dict(self):
        dict_list = [{"a": 1}, {"a": 2, "b": 3}, {"b": 4, "c": 0}]

        self.assertEqual(common.update_dict(dict_list), {"a": 2, "b": 4, "c": 0})
        self.assertEqual(common.update_dict(dict_list, int.__add__), {"a": 3, "b": 7, "c": 0})

    def test_int_parser(self):
        tests = ["0", "00000", "-121", "-0"]
        fail_tests = ["a031", "--0231", "0123a"]
        tests_results = [0, 0, -121, 0]

        success, result = common.common_parsers[int].runTests(tests, printResults=False)
        fail, _ = common.common_parsers[int].runTests(fail_tests, failureTests=True, printResults=False)

        self.assertTrue(success)
        self.assertEqual(tests_results, [i[1][0] for i in result])
