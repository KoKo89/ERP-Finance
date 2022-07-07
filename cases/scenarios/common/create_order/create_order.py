from datetime import date
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import send_api


def create_order(token, data_path, project, customer, recipient_name, recipient_phone, recipient_province, recipient_city, 
                 recipient_county, recipient_line, staff, biz_staff, order_type, memo_order_no, urgent, order_memo, sku_nos, customer_department=''):
    '''
    token：权限\n
    data_path：测试数据json文件的路径\n
    =======================================
    
    
    新增接单时必填项：
    ========================
    project：项目\n
    customer：客户\n
    recipient_name：收货人\n
    recipient_phone：收货电话\n
    recipient_province：收货地址-省\n
    recipient_city：收货地址-市\n
    recipient_county：收货地址-区\n
    recipient_line：收货地址-详情\n
    staff：业务员\n
    biz_staff：商务员\n
    order_type：业务类型（0：常规单，1：赠品单，2：积分单）\n
    memo_order_no：备注订单号\n
    urgent：紧急订单（False：否，True：是）\n
    order_memo：订单备注\n
    sku_nos：商品编号,list类型\n
    =======================================
    
    新增接单时非必填项：
    ========================
    customer_department：客户部门\n
    '''
    
    #发送get_project api
    with open(file=data_path, mode="r", encoding="utf-8") as f:
        old_data = json.load(f)
        old_data['get_project']['body']['name'] = project
        
    with open(file="test.json", mode="w", encoding="utf-8") as f:
        json.dump(old_data, f)
            
    response = send_api.sendApi(data_path, "get_project", token)
    project_id = response["data"][0]["id"]
        
        
    #发送get_customer api
    with open(file=data_path, mode="r", encoding="utf-8") as f:
        old_data = json.load(f)
        old_data['get_customer']['body']['customerName'] = customer
        old_data['get_customer']['body']['projectId'] = project_id
        
    with open(file="test.json", mode="w", encoding="utf-8") as f:
            json.dump(old_data, f)
        
    response = send_api.sendApi(data_path, "get_customer", token)
    customer_id = response["data"][0]["id"]

    
    #发送get_customerDepartment api
    if customer_department != '':
        with open(file=data_path, mode="r", encoding="utf-8") as f:
            old_data = json.load(f)
            old_data['get_customer']['body']['url'] += str(customer_id)
            
        with open(file="test.json", mode="w", encoding="utf-8") as f:
                json.dump(old_data, f)
            
        response = send_api.sendApi(data_path, "get_customerDepartment", token)
        for department in response['data']:
            if department['name'] == customer_department:
                customerDepartment_id = department['id']
    else:
        customerDepartment_id = ''
    
    
    #获取地址-省(北京)
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_province", token)
    province_id = response["data"][0]["id"]
    
    #获取地址-市(北京)
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_region", token)
    city_id = response["data"][0]["id"]
    
    #获取地址-区(东城区)
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_country", token)
    country_id = response["data"][0]["id"]
    
    #获取业务员
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_staff", token)
    staff_id = response["data"][0]["id"]
    
    #获取商务员
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_bizStaff", token)
    bizStaff_id = response["data"][0]["id"]
    
    #获取仓库
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_warehouse", token)
    for warehouse in response["data"]:
        if warehouse["name"] == '曹红玉':
            warehouse_id = warehouse["id"]
            
    #获取商品
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_sku", token)
    itemQty = 5;
    currentDiscount = 100;
    currentPrice = response["data"][0]['websitePrice'] * float(currentDiscount) * 0.01;
    amount = itemQty * float(currentPrice);
    
    itemList = []
    sku = {
        "serverId": "",
        "skuName": response["data"][0]['skuName'],
        "currentDiscount": "100.00",
        "currentPrice": str(currentPrice),
        "itemMemo": "商品备注",
        "itemQty": 1,
        "previousPrice": response["data"][0]['previousPrice'],
        "skuId": response["data"][0]['skuId'],
        "skuNo": response["data"][0]['skuNo'],
        "options": [],
        "skuModel": response["data"][0]['skuModel'],
        "unit": response["data"][0]["unit"],
        "websitePrice": str(response["data"][0]['websitePrice']),
        "negotiatedPrice": response["data"][0]['negotiatedPrice'],
        "negotiatedDiscount": response["data"][0]['negotiatedDiscount'],
        "amount": str(amount),
        "availableQty": response["data"][0]['availableInventory'],
        "costTax": response["data"][0]['costTax'],
        "totalPrice": str(amount)
    }
    itemList.append(sku)
    
    
    #提交订单
    expectedDeliveryDate = date(date.today().year, date.today().month, date.today().day + 1)
    expectedDeliveryDate = str(expectedDeliveryDate)
    body = {'itemList': itemList,
            'customerId': customer_id,  # 客户id
            'customerUserGroupId': customerDepartment_id,  # 客户用户组id(customerDepartment的id)
            'customerUserId': '',  # 客户采购人id（user表id）
            'deliveryMemo': '',  # 发货备注，永远是空
            'expectedDeliveryDate': '2020-07-06',  # 期望配送日期
            'orderMemo': "订单备注",  # 订单备注
            'orderType': 0,  # 业务类型（0：常规单，1：赠品单，2：积分单）
            'packageMemo': '',  # XXXX备注
            'packageType': '',  # XXXX类型
            'projectId': project_id,
            'receiveType': '',  # 目前设置为空
            'recipientAddressProvinceId': province_id,  # 地址-省
            'recipientAddressCityId': city_id,  # 地址-市
            'recipientAddressCountyId': country_id,  # 地址-区
            'recipientAddressLine': '详细地址测试',  # 地址-详细
            'recipientName': 'CHY',  # 收货人
            'recipientPhone': '121212121',  # 收货人电话
            'staffId': staff_id,  # 业务员id
            'bizStaffId': bizStaff_id,  # 商务员id
            'urgents': False,  # 是否紧急（false：否，true：是）
            'urgent': 0,  # 是否紧急（0：否，1：是）
            'orderVisibleAtFront': 0,
            'memoOrderNo': "111111",  # 备注订单号
            'serverId': '22222'  # 备注订单号
            }
    response = send_api.sendApi("./cases/data/common/get_customer.json", "get_sku", token)