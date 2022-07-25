import json
from datetime import date
import time
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from common import login_with_ui, call_api, checkPoint, connect_mysql
from cases.common import order

class Accounts_receivable(checkPoint.CheckPoint):
    
    def setUp(self):
        #获取token
        login_with_ui.get_user_info()
        
    
    def test_syc_order(self):
        
        #获取用户信息
        with open('./configuration/user_info.json', 'r+', encoding='utf-8') as f:
            user_info = json.loads(f.read())
            print(user_info)
            token = user_info['token']
            user_id = user_info['user_id']
            organization_id = user_info['organization_id']
            organization_name = user_info['organization_name']
            real_name = user_info['real_name']
            mobile = user_info['mobile']
        
        #读取应收账款api json文件    
        with open(file='./cases/finance/accounts_receivable/accounts_receivable.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
        
        #创建订单
        new_order = order.Order(token, user_id, organization_id, real_name, mobile)
        order_no = new_order.create_order(project='测试CHY', customer='测试CHY-央企', warehouse= '曹红玉', skus=[{"no":"10066773", "num":5}, {"no":"10055721", "num":5}])
        print(order_no)
        
        order_no = order_no
        mycursor = connect_mysql.leadingDB.cursor()
        mycursor.execute("SELECT * FROM `Order` WHERE `no` = %s", (order_no,))
        myresult = mycursor.fetchall()
        print(myresult)
        order_id = myresult[0][0]
        project_id = myresult[0][5]
        partyBId = myresult[0][6]
        partyBName = myresult[0][7]
        customer_id = myresult[0][9]
        recipient_provinceId = myresult[0][14]
        recipient_cityId = myresult[0][15]
        recipient_countyId = myresult[0][16]
        staff_id = myresult[0][19]
        amount = myresult[0][27]
        staff_name = myresult[0][51]
        
        # mycursor.execute("SELECT * FROM OrderItem WHERE orderId = %s", (order_id,))
        # myresult = mycursor.fetchall()
        
        
        
        mycursor = connect_mysql.userDb.cursor()
        mycursor.execute("SELECT * FROM Customer WHERE `name` = '测试CHY-央企'")
        myresult = mycursor.fetchall()
        customer_no = myresult[0][22]
        
        
        '''
        发送syc_order api，同步订单, 并验证同步成功
        '''
        #发送syc_order api，同步订单
        # time.sleep(300)
        today = date(date.today().year, date.today().month, date.today().day)
        url = apis[0]["syc_order"]['url']
        body = json.dumps(apis[0]["syc_order"]['body'], ensure_ascii=False) % (today, today)
        response = call_api.post(url, body, token)
        
        #验证同步接口相应成功
        self.checkAssertEqual(response['message'], "请求成功!")
        self.checkAssertGreaterEqual(int(response['data']), 1)
        
        #发送receivable_orderInfo api，应收账款汇总表获取该订单
        url = apis[0]["receivable_orderInfo"]['url']
        body = json.dumps(apis[0]["receivable_orderInfo"]['body'], ensure_ascii=False) % (order_no)
        response = call_api.post(url, body, token)
        
        
        
        #验证订单信息
        self.checkAssertEqual(response['data']['total'], 1, '单据总数')
        self.checkAssertEqual(len(response['data']['items']), 1, '单据总数')
        self.checkAssertEqual(response['data']['items'][0]['amountPaid'], 0, '付款金额')
        self.checkAssertEqual(response['data']['items'][0]['area'], '北京市-北京市-朝阳区', '收获区域')
        self.checkAssertEqual(response['data']['items'][0]['billStatusText'], '未对账', '对账状态文本')
        self.checkAssertEqual(response['data']['items'][0]['billTime'], None, '对账时间')
        self.checkAssertEqual(response['data']['items'][0]['bizType'], 1, '单据类型')
        self.checkAssertEqual(response['data']['items'][0]['bizTypeName'], '销售订单', '单据类型名称')
        self.checkAssertEqual(response['data']['items'][0]['closeStatus'], 0, '关闭状态')
        self.checkAssertEqual(response['data']['items'][0]['closeStatusText'], '未关闭', '关闭状态文本')
        self.checkAssertEqual(response['data']['items'][0]['createUserId'], user_id, '创建用户id')
        self.checkAssertEqual(response['data']['items'][0]['createUserName'], real_name, '创建用户名称')
        self.checkAssertEqual(response['data']['items'][0]['customerDepartmentId'], 0, '客户部门id')
        self.checkAssertEqual(response['data']['items'][0]['customerDepartmentName'], '', '客户部门名称')
        self.checkAssertEqual(response['data']['items'][0]['customerId'], customer_id, '客户id')
        self.checkAssertEqual(response['data']['items'][0]['customerName'], '测试CHY-央企', '客户名称')
        self.checkAssertEqual(response['data']['items'][0]['customerNo'], customer_no, '客户编号')
        self.checkAssertEqual(response['data']['items'][0]['customerOrderNo'], '', '外部订单号')
        self.checkAssertEqual(response['data']['items'][0]['customerReceiptAddress'], '北京市-北京市-朝阳区-大羊坊路新华国际广场', '收获地址')
        self.checkAssertEqual(response['data']['items'][0]['customerType'], 0, '客户性质')#（-1: - , 0：央企，1：国企，2：外企，3：民企，4：政府，5：军队，6：事业单位）
        self.checkAssertEqual(response['data']['items'][0]['customerTypeName'], None, '客户性质名称')
        self.checkAssertEqual(response['data']['items'][0]['dimensionText'], '', '对账维度')
        # self.checkAssertEqual(response['data']['items'][0]['documentId'], '', '单据id')
        self.checkAssertEqual(response['data']['items'][0]['documentNo'], order_no, '单据号')
        self.checkAssertEqual(response['data']['items'][0]['finishTime'], str(today), '完成日期')
        self.checkAssertEqual(response['data']['items'][0]['getRecipientAddressCityName'], '北京市', '收获地址-市')
        self.checkAssertEqual(response['data']['items'][0]['getRecipientAddressCountyName'], '朝阳区', '收获地址-区')
        self.checkAssertEqual(response['data']['items'][0]['getRecipientAddressProvinceName'], '北京市', '收获地址-省')
        self.checkAssertEqual(response['data']['items'][0]['invoiceStatusText'], '未开票', '开票状态')#（0：未开票，1：部分开票，2：已开票）
        self.checkAssertEqual(response['data']['items'][0]['invoiceTime'], None, '开票时间')
        self.checkAssertEqual(response['data']['items'][0]['logStatus'], 0, '日志状态')#（0：没有日志，1：有日志)
        self.checkAssertEqual(response['data']['items'][0]['memo'], '', '备注')
        self.checkAssertEqual(response['data']['items'][0]['memoOrderNo'], '', '备注订单号')
        self.checkAssertEqual(response['data']['items'][0]['number'], None, 'number')
        self.checkAssertEqual(response['data']['items'][0]['oldErpOrderId'], None, '旧系统订单号')
        self.checkAssertEqual(response['data']['items'][0]['orderAccountReceiveable'], amount, "应收金额")
        self.checkAssertEqual(response['data']['items'][0]['orderAmountInvoiced'], 0, '已开票金额')
        self.checkAssertEqual(response['data']['items'][0]['orderAmountNotInvoiced'], amount, '未开票金额')
        self.checkAssertEqual(response['data']['items'][0]['orderAmountNotSettled'], amount, '未对账金额')
        self.checkAssertEqual(response['data']['items'][0]['orderAmountReceived'], 0, '收款金额')
        self.checkAssertEqual(response['data']['items'][0]['orderAmountReceivedBalance'], amount, '应收余额')
        self.checkAssertEqual(response['data']['items'][0]['orderAmountSettled'], 0, '已对账金额')
        self.checkAssertEqual(response['data']['items'][0]['orderCreateTime'], str(today), '订单创建时间')
        self.checkAssertEqual(response['data']['items'][0]['orderQty'], 10, '订单数量')
        self.checkAssertEqual(response['data']['items'][0]['orderQtyInvoiced'], 0, '已开票数量')
        self.checkAssertEqual(response['data']['items'][0]['orderQtyNotInvoiced'], 10, '未开票数量')
        self.checkAssertEqual(response['data']['items'][0]['orderQtyNotSettled'], 10, '未对账数量')
        self.checkAssertEqual(response['data']['items'][0]['orderQtySettled'], 0, '已对账数量')
        self.checkAssertEqual(response['data']['items'][0]['orderType'], 0, '业务类型')#（0：常规单，1：赠品单，2：积分单）
        self.checkAssertEqual(response['data']['items'][0]['partyBId'], partyBId, '项目乙方Id')
        self.checkAssertEqual(response['data']['items'][0]['partyBName'], partyBName, '项目乙方名字')
        self.checkAssertEqual(response['data']['items'][0]['paymentStatus'], 0, '付款状态')#（0：未付款，1：部分付款，2：已付款)
        self.checkAssertEqual(response['data']['items'][0]['paymentStatusText'], '未付款', '付款状态')#（已付款、未付款、部分付款)
        self.checkAssertEqual(response['data']['items'][0]['paymentTime'], None, '付款时间')
        self.checkAssertEqual(response['data']['items'][0]['projectId'], project_id, '项目Id')
        self.checkAssertEqual(response['data']['items'][0]['projectName'], '测试CHY', '项目名字')
        self.checkAssertEqual(response['data']['items'][0]['receiptTime'], None, '收款时间')
        self.checkAssertEqual(response['data']['items'][0]['recipientAddressCityId'], recipient_cityId, '收货-市id')
        self.checkAssertEqual(response['data']['items'][0]['recipientAddressCountyId'], recipient_countyId, '区id')
        self.checkAssertEqual(response['data']['items'][0]['recipientAddressLine'], '大羊坊路新华国际广场', '收货-详细地址')
        self.checkAssertEqual(response['data']['items'][0]['recipientAddressProvinceId'], recipient_provinceId, '收货-省id')
        self.checkAssertEqual(response['data']['items'][0]['recipientName'], 'chy', '收货人')
        self.checkAssertEqual(response['data']['items'][0]['recipientPhone'], '123456', '收货人联系方式')
        self.checkAssertEqual(response['data']['items'][0]['relationDocumentId'], None, '关联单号ID')
        self.checkAssertEqual(response['data']['items'][0]['relationDocumentNo'], None, '关联单号')
        self.checkAssertEqual(response['data']['items'][0]['serverId'], organization_id, '服务方Id')
        self.checkAssertEqual(response['data']['items'][0]['serverName'], organization_name, '服务方名字')
        self.checkAssertEqual(response['data']['items'][0]['staffId'], staff_id, '业务员Id')
        self.checkAssertEqual(response['data']['items'][0]['staffName'], staff_name, '业务员名字')
        self.checkAssertEqual(response['data']['items'][0]['writeOffStatusText'], '未收款', '收款核销状态')#（0：未收款，1：部分收款，2：已收款）
        self.checkAssertEqual(response['data']['items'][0]['writeOffTime'], None, '核销时间')
        
        self.checkTestResult()