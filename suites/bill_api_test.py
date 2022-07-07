import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import login_with_ui, send_api
from BeautifulReport import BeautifulReport

class BillApiTest(unittest.TestCase): #测试方法类
    
    def setUp(self) -> None:
        print("start==============")
        login_with_ui.get_token()
    

    def tearDown(self) -> None:
        print("stop==============")
    

    def test_listApi(self):
        print("testListApi============")
        with open('./configuration/token.json', 'r+') as f:
            token = f.read()
        response = send_api.sendApi("./data/bill_apis.json", "Bill_list api", token)
        self.assertEqual(response['message'], "请求成功!")
    
    def test_deleteApi(self):
        print("testDeleteApi============")
        with open('./configuration/token.json', 'r+') as f:
            token = f.read()
        response = send_api.sendApi("./data/bill_apis.json", "Bill_delete api", token)
        self.assertEqual(response['message'], "请求成功!")


if __name__ == '__main__':
    #使用TestSuit控制用例顺序，用例执行顺序是添加的顺序
    tests = [BillApiTest('test_listApi'),BillApiTest('test_deleteApi')]
    suites = unittest.TestSuite()
    suites.addTests(tests)
    
    # runner = unittest.TextTestRunner()
    # runner.run(suites)
    
    file_path = r'./reports' #定义报告所放置的位置
    result = BeautifulReport(suites)
    result.report(description='测试deafult报告', filename='测试报告', report_dir=file_path, theme='theme_default')