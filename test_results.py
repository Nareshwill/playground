import unittest


def get_result(tp, fp, fn):
    if int(tp) > (int(fp) + int(fn)):
        result = 'PASS'
        remark = ''
        return result, remark
    else:
        result = 'FAIL'
        remark = "TP is less than FP + FN"
        return result, remark


class TestGetResult(unittest.TestCase):
    def test_get_result_pass_response(self):
        result, remark = get_result(tp=57, fp=20, fn=10)
        self.assertEqual(result, 'PASS')
        self.assertEqual(remark, '')

    def test_get_result_fail_response(self):
        result, remark = get_result(tp=20, fp=30, fn=40)
        self.assertEqual(result, 'FAIL')
        self.assertEqual(remark, 'TP is less than FP + FN')
