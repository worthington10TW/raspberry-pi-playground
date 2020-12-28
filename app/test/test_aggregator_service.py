# #!/usr/bin/env python3
#
# import unittest
#
# from app.ci_gateway import constants as r
# from app import aggregator_service as s
#
#
# def return_pass():
#     return dict(status=r.Result.PASS)
#
#
# def return_fail():
#     return dict(status=r.Result.FAIL)
#
#
# def return_running():
#     return dict(status=r.Result.RUNNING)
#
#
# class GithubTests(unittest.TestCase):
#
#     def test_is_running(self):
#         actions = [
#             {"action": return_pass},
#             {"action": return_fail},
#             {"action": return_running}
#         ]
#         result = s.AggregatorService(actions).run()
#         self.assertEqual(True, result["is_running"])
#
#     def test_is_not_running(self):
#         actions = [
#             {"action": return_pass},
#             {"action": return_fail}
#         ]
#         result = s.AggregatorService(actions).run()
#         self.assertEqual(False, result["is_running"])
#
#     def test_contains_failed(self):
#         actions = [
#             {"action": return_pass},
#             {"action": return_fail},
#         ]
#         result = s.AggregatorService(actions).run()
#         self.assertEqual(r.Result.FAIL, result["status"])
#
#     def test_all_pass(self):
#         actions = [
#             {"action": return_pass},
#             {"action": return_pass},
#             {"action": return_running},
#         ]
#         result = s.AggregatorService(actions).run()
#         self.assertEqual(r.Result.PASS, result["status"])
#
#     def test_no_results(self):
#         actions = [
#             {"action": return_running}
#         ]
#         result = s.AggregatorService(actions).run()
#         self.assertEqual(r.Result.NONE, result["status"])
#
#
# if __name__ == '__main__':
#     unittest.main()
