import unittest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import login_with_ui, send_api
import BeautifulReport

class BillApiTest(unittest.TestCase): #测试方法类
    
    def setUp(self) -> None:
        print("start==============")
    

    def tearDown(self) -> None:
        print("stop==============")
    

    def test_listApi(self):
        print("testListApi============")
        token = login_with_ui.get_token()
        response = send_api.sendApi("./all_apis/bill_apis.json", "Bill_list api", token)
        self.assertEqual(response['message'], "请求成功!")
    
    def test_deleteApi(self):
        print("testDeleteApi============")
        token = login_with_ui.get_token()
        response = send_api.sendApi("./all_apis/bill_apis.json", "Bill_delete api", token)
        self.assertEqual(response['message'], "请求成功!")
        

# if __name__ == 'main':
#     tests = [BillApiTest("test_listApi"), BillApiTest("test_deleteApi")]
#     print("tests=" + tests)
#     suite = unittest.TestSuite()
#     suite.addTests(tests)
    
#     runner = unittest.TextTestRunner()
#     runner.run(suite)


if __name__ == '__main__':
    #使用TestSuit控制用例顺序，用例执行顺序是添加的顺序
    tests = [BillApiTest('test_listApi'),BillApiTest('test_deleteApi')]
    suites = unittest.TestSuite()
    suites.addTests(tests)
    
    #file_path = r'./Reports' #定义报告所放置的位置
    runner = unittest.TextTestRunner()
    runner.run(suites)
    
    # result = BeautifulReport(suite)
    # result.report(description='测试deafult报告', filename='测试报告', report_dir=file_path, theme='theme_default')