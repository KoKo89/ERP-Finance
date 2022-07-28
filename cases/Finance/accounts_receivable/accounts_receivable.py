import json
from datetime import date
import time
import sys
import os

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from common import db_connect, login_with_ui, call_api
from cases.common import order
from configuration import environment_exection


class Test_receivable():
    #获取token
    login_with_ui.get_user_info()
        
        
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
            
    #创建订单
    global order_no
    new_order = order.Order(token, user_id, organization_id, real_name, mobile)
    order_no = new_order.create_order(project='测试CHY', customer='测试CHY-央企', warehouse= '曹红玉', skus=[{"no":"10066773", "num":5}, {"no":"10055721", "num":5}])
            
    #创建发货单
    global delivery_no
    global delivery_id
    delivery_no, delivery_id = new_order.generate_delivery(order_no=order_no, warehouse='曹红玉', delivery_sku=[{"no":"10066773", "num":5}, {"no":"10055721", "num":5}])
            
    #发货单出库
    new_order.out_warehouse(delivery_no)
            
    #创建退货单
    global returnorder_no
    global returnorder_id
    new_order.confirmed_delivery(delivery_id)
    returnorder_no, returnorder_id = new_order.return_order(delivery_no, delivery_id, return_sku=[{"no":"10066773", "num":5}, {"no":"10055721", "num":5}])
    time.sleep(2)
            
            
    #连接数据库
    # global leadingDB
    # global financeDB
    # global userDb
    leadingDB = db_connect.db_connect(environment_exection.leadingDB).cursor()
    financeDB = db_connect.db_connect(environment_exection.financeDB).cursor()
    userDb = db_connect.db_connect(environment_exection.userDb).cursor()

    leadingDB.execute("SELECT * FROM `Order` WHERE `no` = %s", (order_no,))
    myresult = leadingDB.fetchall()
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
    
    leadingDB.execute("SELECT * FROM `OrderDelivery` WHERE orderDeliveryNo = %s", (delivery_no,))
    myresult = leadingDB.fetchall()
    print(myresult)
    delivery_amount = -myresult[0][7]
    
    leadingDB.execute("SELECT * FROM ReturnOrder WHERE returnOrderNo =  %s", (returnorder_no,))
    myresult = leadingDB.fetchall()
    print(myresult)
    return_amount = -myresult[0][7]
                
    userDb.execute("SELECT * FROM Customer WHERE `name` = '测试CHY-央企'")
    myresult = userDb.fetchall()
    customer_no = myresult[0][22]
            

    def test_order(self):
        '''
        发送syc_order api，同步订单, 并验证同步成功
        '''
        
        #获取用户信息
        with open('./configuration/user_info.json', 'r+', encoding='utf-8') as f:
            user_info = json.loads(f.read())
            print(user_info)
            token = user_info['token']
        
        #读取应收账款api json文件    
        with open(file='./cases/finance/accounts_receivable/accounts_receivable.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
        
        #发送syc_order api，同步订单
        # time.sleep(300)
        today = date(date.today().year, date.today().month, date.today().day)
        url = apis[0]["syc_order"]['url']
        body = json.dumps(apis[0]["syc_order"]['body'], ensure_ascii=False) % (today, today)
        response = call_api.post(url, body, token)
            
        #验证同步接口相应成功
        assert response['message'] == "请求成功!", "同步接口请求成功"
            
        #发送receivable_orderInfo api，应收账款汇总表获取该订单
        url = apis[0]["receivable_orderInfo"]['url']
        body = json.dumps(apis[0]["receivable_orderInfo"]['body'], ensure_ascii=False) % (order_no)
        response = call_api.post(url, body, token)
            
        #验证订单信息
        assert response['data']['total'] == 1, "只有一个订单"


        
    def test_delivery(self):
        '''
        发送syc_order api，同步发货单, 并验证同步成功
        '''
        
        #获取用户信息
        with open('./configuration/user_info.json', 'r+', encoding='utf-8') as f:
            user_info = json.loads(f.read())
            print(user_info)
            token = user_info['token']
            
        #读取应收账款api json文件    
        with open(file='./cases/finance/accounts_receivable/accounts_receivable.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
            
        #syc_delivery api，同步发货单
        today = date(date.today().year, date.today().month, date.today().day)
        url = apis[0]["syc_delivery"]['url']
        body = json.dumps(apis[0]["syc_delivery"]['body'], ensure_ascii=False) % (today, today)
        response = call_api.post(url, body, token)
            
        #验证同步接口相应成功
        assert response['message'] == "请求成功!", "同步接口请求成功"
            
        #receivable_deliveryInfo api，应收账款汇总表获取该订单
        url = apis[0]["receivable_deliveryInfo"]['url']
        body = json.dumps(apis[0]["receivable_deliveryInfo"]['body'], ensure_ascii=False) % (delivery_no)
        response = call_api.post(url, body, token)
            
            
            
        #验证订单信息
        assert response['data']['total'] == 1, "只有一个发货单"

        
