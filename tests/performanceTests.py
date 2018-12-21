import time
from datetime import datetime
from unittest import TestCase
from parameterized import parameterized
from alias import *


class ArgumentationFrameworkTests(TestCase):
    stable_prefix = './frameworks/stable/'
    complete_prefix = './frameworks/complete/'
    preferred_prefix = './frameworks/preferred/'
    five_sec = float(5)

    def setUp(self):
        """METHOD_SETUP"""

    def tearDown(self):
        """METHOD_TEARDOWN"""

    @parameterized.expand([
        [stable_prefix + 'stable1.tgf', five_sec],
        [stable_prefix + 'stable2.tgf', five_sec],
        [stable_prefix + 'stable3.tgf', five_sec],
        [stable_prefix + 'stable4.tgf', five_sec],
        [stable_prefix + 'stable5.tgf', five_sec],
        [stable_prefix + 'stable6.tgf', five_sec],
    ])
    def stable_extension_test(self, framework, maximal_duration):
        started_at = time.time()
        argumentation_framework = alias.read_tgf(framework)
        argumentation_framework.get_stable_extension()
        finished_at = time.time()
        assert finished_at - started_at < maximal_duration, 'Execution time took ' + str(finished_at - started_at)

    # @parameterized.expand([
    #     [complete_prefix + 'preferred1.tgf', complete_prefix + 'complete1answer'],
    #     [complete_prefix + 'complete2.tgf', complete_prefix + 'complete2answer'],
    #     [complete_prefix + 'complete3.tgf', complete_prefix + 'complete3answer'],
    #     [complete_prefix + 'complete4.tgf', complete_prefix + 'complete4answer'],
    #     [complete_prefix + 'complete5.tgf', complete_prefix + 'complete5answer'],
    #     [complete_prefix + 'complete6.tgf', complete_prefix + 'complete6answer'],
    # ])
    # def complete_extension_test(self, framework, solution):
    #     argumentation_framework = alias.read_tgf(framework)
    #     actual_complete = argumentation_framework.get_complete_extension()
    #     expected_complete = TestHelper.read_solution_from_file(solution)
    #     TestHelper.assertListsEqual(expected_complete, actual_complete)
    # # #
    @parameterized.expand([
        [preferred_prefix + 'preferred1.tgf', five_sec],
        [preferred_prefix + 'preferred2.tgf', five_sec],
        [preferred_prefix + 'preferred3.tgf', five_sec],
        [preferred_prefix + 'preferred4.tgf', five_sec],
        [preferred_prefix + 'preferred5.tgf', five_sec],
        [preferred_prefix + 'preferred6.tgf', five_sec],
    ])
    def preferred_extension_test(self, framework, maximal_duration):
        started_at = datetime.now()
        argumentation_framework = alias.read_tgf(framework)
        actual_preferred = argumentation_framework.get_preferred_extension()
        finished_at = datetime.now()
        total_seconds = (finished_at - started_at).total_seconds()
        assert total_seconds < maximal_duration, 'Execution time took ' + str(finished_at - started_at)