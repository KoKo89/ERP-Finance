import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import login_with_ui
from bill_api import *
import BeautifulReport

class BillApiTest(unittest.TestCase): #测试方法类
    
    
    token = login_with_ui.get_token()
    def __init__(self, token):
        self.token = token

    def setUp(self) -> None:
        
        print("start==============")
    

    def tearDown(self) -> None:
        print("stop==============")
    

    def test_listApi(self):
        print("testListApi============")
        
        self.assertEqual(bill_list(self.token), "请求成功!")
    
    def test_deleteApi(self):
        print("testDeleteApi============")
        
        self.assertEqual(bill_delete(self.token), "请求成功!")
        

# if __name__ == 'main':
#     tests = [BillApiTest("test_listApi"), BillApiTest("test_deleteApi")]
#     print("tests=" + tests)
#     suite = unittest.TestSuite()
#     suite.addTests(tests)
    
#     runner = unittest.TextTestRunner()
#     runner.run(suite)


if __name__ == '__main__':
    #使用TestSuit控制用例顺序，用例执行顺序是添加的顺序
    tests = [BillApiTest('test_listApi'), BillApiTest('test_deleteApi')]
    suites = unittest.TestSuite()
    suites.addTests(tests)
    
    #file_path = r'./Reports' #定义报告所放置的位置
    runner = unittest.TextTestRunner()
    runner.run(suites)
    
    # result = BeautifulReport(suite)
    # result.report(description='测试deafult报告', filename='测试报告', report_dir=file_path, theme='theme_default')