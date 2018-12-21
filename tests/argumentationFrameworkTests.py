from unittest import TestCase
from parameterized import parameterized
from alias import *
from tests import TestHelper


class ArgumentationFrameworkTests(TestCase):
    stable_prefix = './frameworks/stable/'
    complete_prefix = './frameworks/complete/'
    preferred_prefix = './frameworks/preferred/'
    
    def setUp(self):
        """METHOD_SETUP"""

    def tearDown(self):
        """METHOD_TEARDOWN"""

    @parameterized.expand([
        [stable_prefix + 'stable1.tgf', stable_prefix + 'stable1answer'],
        [stable_prefix + 'stable2.tgf', stable_prefix + 'stable2answer'],
        [stable_prefix + 'stable3.tgf', stable_prefix + 'stable3answer'],
        [stable_prefix + 'stable4.tgf', stable_prefix + 'stable4answer'],
        [stable_prefix + 'stable5.tgf', stable_prefix + 'stable5answer'],
        [stable_prefix + 'stable6.tgf', stable_prefix + 'stable6answer'],
    ])
    def compute_stable_extensions(self, framework, solution):
        argumentation_framework = alias.read_tgf(framework)
        actual_stable = argumentation_framework.get_stable_extension()
        expected_stable = TestHelper.read_solution_from_file(solution)
        TestHelper.assert_lists_equal(expected_stable, actual_stable)

    @parameterized.expand([
        [complete_prefix + 'complete1.tgf', complete_prefix + 'complete1answer'],
        [complete_prefix + 'complete2.tgf', complete_prefix + 'complete2answer'],
        [complete_prefix + 'complete3.tgf', complete_prefix + 'complete3answer'],
        [complete_prefix + 'complete4.tgf', complete_prefix + 'complete4answer'],
        [complete_prefix + 'complete5.tgf', complete_prefix + 'complete5answer'],
        [complete_prefix + 'complete6.tgf', complete_prefix + 'complete6answer'],
    ])
    def compute_all_complete_extensions(self, framework, solution):
        argumentation_framework = alias.read_tgf(framework)
        actual_complete = argumentation_framework.get_complete_extension()
        expected_complete = TestHelper.read_solution_from_file(solution)
        TestHelper.assert_lists_equal(expected_complete, actual_complete)

    @parameterized.expand([
        [preferred_prefix + 'preferred1.tgf', preferred_prefix + 'preferred1answer'],
        [preferred_prefix + 'preferred2.tgf', preferred_prefix + 'preferred2answer'],
        [preferred_prefix + 'preferred3.tgf', preferred_prefix + 'preferred3answer'],
        [preferred_prefix + 'preferred4.tgf', preferred_prefix + 'preferred4answer'],
        [preferred_prefix + 'preferred5.tgf', preferred_prefix + 'preferred5answer'],
        [preferred_prefix + 'preferred6.tgf', preferred_prefix + 'preferred6answer'],
    ])
    def compute_all_preferred_extensions(self, framework, solution):
        argumentation_framework = alias.read_tgf(framework)
        actual_preferred = argumentation_framework.get_preferred_extension()
        expected_preferred = TestHelper.read_solution_from_file(solution)
        TestHelper.assert_lists_equal(expected_preferred, actual_preferred)
