import unittest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import login_with_ui, call_api
from BeautifulReport import BeautifulReport
from cases.common import create_order, delivery_order

# class BillApiTest(unittest.TestCase): #测试方法类
    
#     def setUp(self) -> None:
#         print("start==============")
#         login_with_ui.get_user_info()
    

#     def tearDown(self) -> None:
#         print("stop==============")
    

#     def test_listApi(self):
#         print("testListApi============")
#         with open('./configuration/token.json', 'r+') as f:
#             token = json.loads(f.read())
#         with open(file='./cases/data/bill_apis.json', mode="r", encoding="utf-8") as f:
#             apis = json.loads(f.read())
#             print('打开文件')
        
#         #response = send_api.sendApi("./cases/data/bill_apis.json", "Bill_list api", token)
#         url = apis["Bill_list api"]['url']
#         body = apis["Bill_list api"]['body']
#         response = call_api.post(url=url, body=body, token=token)
#         self.assertEqual(response['message'], "请求成功!")


# if __name__ == '__main__':
#     #使用TestSuit控制用例顺序，用例执行顺序是添加的顺序
#     tests = [BillApiTest('test_listApi')]
#     suites = unittest.TestSuite()
#     suites.addTests(tests)
    
#     # runner = unittest.TextTestRunner()
#     # runner.run(suites)
    
#     file_path = r'./reports' #定义报告所放置的位置
#     result = BeautifulReport(suites)
#     result.report(description='测试deafult报告', filename='测试报告', report_dir=file_path, theme='theme_default')



login_with_ui.get_user_info()
with open('./configuration/user_info.json', 'r+') as f:
            user_info = json.loads(f.read())
            print(user_info)
            token = user_info['token']
            user_id = user_info['user_id']
            organization_id = user_info['organization_id']

# order = create_order.Order(token, user_id, organization_id, './cases/common/create_order.json')
# order_no = order.create_order(project='测试CHY', customer='测试CHY-央企', warehouse= '曹红玉', sku_nos=['10066773'])
# print(order_no)

# delivery = delivery_order.Delivery(token, user_id, organization_id, './cases/common/delivery_order.json')
# delivery_id = delivery.generate_delivery(order_no='XSDD20220713000001', warehouse='曹红玉', delivery_sku=[{"no":"10066773", "num":1}], auto_invoice=1, 
#                                       invoice_type=1, need_post=1,need_receipt=1,tax_sign=1)
# print(delivery_id)