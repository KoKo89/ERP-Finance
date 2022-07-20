import json
from datetime import date
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from common import login_with_ui, call_api
from cases.common import order

class Accounts_receivable(unittest.TestCase):
    
    def setUp(self):
        login_with_ui.get_user_info()
        
    def test_syc_order(self):
        
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
        new_order = order.Order(token, user_id, organization_id, real_name, mobile)
        order_no = new_order.create_order(project='测试CHY', customer='测试CHY-央企', warehouse= '曹红玉', skus=[{"no":"10066773", "num":5}, {"no":"10055721", "num":5}])
        print(order_no)
        
        '''
        发送syc_order api，同步订单, 并验证同步成功
        '''
        #发送syc_order api，同步订单
        today = date(date.today().year, date.today().month, date.today().day)
        url = apis[0]["syc_order"]['url']
        body = json.dumps(apis[0]["syc_order"]['body'], ensure_ascii=False) % (today, today)
        response = call_api.post(url, body, token)
        
        #验证同步接口相应成功
        self.assertEqual(response['message'], "请求成功")
        self.assertGreaterEqual(response['data'], 1)
        
        #发送receivable_orderInfo api，应收账款汇总表获取该订单
        url = apis[0]["receivable_orderInfo"]['url']
        body = json.dumps(apis[0]["receivable_orderInfo"]['body'], ensure_ascii=False) % (order_no)
        response = call_api.post(url, body, token)
        
        #验证订单信息
        self.assertEqual(response['data']['total'], 1)
        self.assertEqual(len(response['data']['items']), 1)
        self.assertEqual(response['data']['items'][0]['amountPaid'], 0)
        self.assertEqual(response['data']['items'][0]['area'], '北京市-北京市-朝阳区')
        self.assertEqual(response['data']['items'][0]['billStatusText'], '未对账')
        self.assertEqual(response['data']['items'][0]['billTime'], None)
        self.assertEqual(response['data']['items'][0]['bizType'], 1)
        self.assertEqual(response['data']['items'][0]['bizTypeName'], '销售订单')
        self.assertEqual(response['data']['items'][0]['closeStatus'], 0)
        self.assertEqual(response['data']['items'][0]['closeStatusText'], '未关闭')
        self.assertEqual(response['data']['items'][0]['createUserId'], user_id)
        self.assertEqual(response['data']['items'][0]['createUserName'], real_name)
        self.assertEqual(response['data']['items'][0]['customerDepartmentId'], 0)
        self.assertEqual(response['data']['items'][0]['customerDepartmentName'], '')
        # self.assertEqual(response['data']['items'][0]['customerId'], 5092)
        self.assertEqual(response['data']['items'][0]['customerName'], '测试CHY-央企')
        # self.assertEqual(response['data']['items'][0]['customerNo'], 105216)
        self.assertEqual(response['data']['items'][0]['customerOrderNo'], '')#外部订单号
        self.assertEqual(response['data']['items'][0]['customerReceiptAddress'], '北京市-北京市-朝阳区-大羊坊路新华国际广场')
        self.assertEqual(response['data']['items'][0]['customerType'], 0)#客户性质（-1: - , 0：央企，1：国企，2：外企，3：民企，4：政府，5：军队，6：事业单位）
        self.assertEqual(response['data']['items'][0]['customerTypeName'], None)
        self.assertEqual(response['data']['items'][0]['dimensionText'], '')#对账维度
        # self.assertEqual(response['data']['items'][0]['documentId'], '')
        self.assertEqual(response['data']['items'][0]['documentNo'], order_no)
        self.assertEqual(response['data']['items'][0]['finishTime'], today)
        self.assertEqual(response['data']['items'][0]['getRecipientAddressCityName'], '北京市')
        self.assertEqual(response['data']['items'][0]['getRecipientAddressCountyName'], '朝阳区')
        self.assertEqual(response['data']['items'][0]['getRecipientAddressProvinceName'], '北京市')
        self.assertEqual(response['data']['items'][0]['invoiceStatusText'], '未开票')#开票状态（0：未开票，1：部分开票，2：已开票）
        self.assertEqual(response['data']['items'][0]['invoiceTime'], None)
        self.assertEqual(response['data']['items'][0]['logStatus'], 0)#日志状态（0：没有日志，1：有日志)
        self.assertEqual(response['data']['items'][0]['memo'], '')#备注
        self.assertEqual(response['data']['items'][0]['memoOrderNo'], '')#备注订单号
        self.assertEqual(response['data']['items'][0]['number'], None)
        self.assertEqual(response['data']['items'][0]['oldErpOrderId'], None)#旧系统订单号
        self.assertEqual(response['data']['items'][0]['orderAccountReceiveable'], 100)#应收金额
        self.assertEqual(response['data']['items'][0]['orderAmountInvoiced'], 0)#已开票金额
        self.assertEqual(response['data']['items'][0]['orderAmountNotInvoiced'], 100)#未开票金额
        self.assertEqual(response['data']['items'][0]['orderAmountNotSettled'], 100)#未对账金额
        self.assertEqual(response['data']['items'][0]['orderAmountReceived'], 0)#收款金额
        self.assertEqual(response['data']['items'][0]['orderAmountReceived'], 0)#收款金额