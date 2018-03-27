from unittest import TestCase
from nose_parameterized import parameterized
from alias import *
from Tests import TestHelper


class ArgumentationFrameworkTests(TestCase):
    prefix = './frameworks/stable/'

    def setUp(self):
        """METHOD_SETUP"""

    def tearDown(self):
        """METHOD_TEARDOWN"""

    @parameterized.expand([
        [prefix + 'stable1.tgf', prefix + 'stable1answer'],
        [prefix + 'stable2.tgf', prefix + 'stable2answer'],
        [prefix + 'stable3.tgf', prefix + 'stable3answer'],
        [prefix + 'stable4.tgf', prefix + 'stable4answer'],
        [prefix + 'stable5.tgf', prefix + 'stable5answer'],
        [prefix + 'stable6.tgf', prefix + 'stable6answer'],
    ])
    def stable_extension_test(self, framework, solution):
        argumentation_framework = alias.read_tgf(framework)
        actual_stable = argumentation_framework.get_stable_extension()
        expected_stable = TestHelper.read_solution_from_file(solution)
        TestHelper.assertListsEqual(expected_stable, actual_stable)
