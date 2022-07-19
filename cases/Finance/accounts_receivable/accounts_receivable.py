from cmath import log
import json
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import login_with_ui, call_api
from cases.common import order

class Accounts_receivable(unittest.TestCase):
    
    def setUp(self):
        login_with_ui.get_user_info()
        
        
    def test_syc_order():
        
        #获取用户信息
        with open('./configuration/user_info.json', 'r+', encoding='utf-8') as f:
            user_info = json.loads(f.read())
            print(user_info)
            token = user_info['token']
            user_id = user_info['user_id']
            organization_id = user_info['organization_id']
            real_name = user_info['real_name']
            mobile = user_info['mobile']
        
        #读取应收账款api json文件    
        with open(file='./cases/finance/accounts_receivable', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
         
        #创建订单    
        order = order.Order(token, user_id, organization_id, real_name, mobile)
        order_no = order.create_order(project='测试CHY', customer='测试CHY-央企', warehouse= '曹红玉', skus=[{"no":"10066773", "num":5}, {"no":"10055721", "num":5}])
        print(order_no)
        
        #同步订单
        url = apis[0]["syc_order"]['url']
        body = json.dumps(apis[0]["syc_order"]['body'], ensure_ascii=False) % (project)
        response = call_api.post(url, body, self.token)
        project_id = response["data"][0]["id"]
        