from datetime import date
import json
from re import S

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import call_api,login_with_ui

class Order:
    
    def __init__(self, token, user_id, organization_id, data_path) :
        self.token = token
        self.user_id = user_id
        self.organization_id = organization_id
        self.data_path = data_path
        
    
    def create_order(self, project, customer, warehouse, sku_nos, customer_department='', staff = '', biz_staff='',
                    recipient_name='chy', recipient_phone='123456', recipient_province='北京市', recipient_city='北京市', recipient_county='朝阳区', 
                    recipient_line='大羊坊路新华国际广场', order_type=0, memo_order_no='', urgent=0, order_memo=''):
        '''  
        必填项：
        ========================
        project：项目\n
        customer：客户\n
        warehouse：仓库名称\n
        sku_nos：商品编号,list类型\n
        =======================================
        
        非必填项：
        ========================
        customer_department：客户部门\n
        staff：业务员，不输入值则默认取登录用户\n
        biz_staff：商务员，不输入值则默认取登录用户\n
        recipient_name：收货人\n
        recipient_phone：收货电话\n
        recipient_province：收货地址-省\n
        recipient_city：收货地址-市\n
        recipient_county：收货地址-区\n
        recipient_line：收货地址-详情\n
        order_type：业务类型（0：常规单，1：赠品单，2：积分单）\n
        memo_order_no：备注订单号\n
        urgent：是否紧急（0：否，1：是）\n
        order_memo：订单备注\n
        '''
        
        #打开json文件
        with open(file=self.data_path, mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
            

        #发送get_project api 
        url = apis["get_project"]['url']
        body = json.dumps(apis["get_project"]['body'], ensure_ascii=False) % (project)
        response = call_api.post(url, body, self.token)
        project_id = response["data"][0]["id"]
            
            
        #发送get_customer api
        url = apis["get_customer"]['url']
        body = json.dumps(apis["get_customer"]['body'], ensure_ascii=False) % (customer, project_id)
        response = call_api.post(url, body, self.token)
        customer_id = response["data"][0]["id"]

        
        #发送get_customerDepartment api
        if customer_department != '':
            url = apis["get_customer"]['url'] % (customer_id)
            response = call_api.get(url, self.token)
            for department in response['data']:
                if department['name'] == customer_department:
                    customerDepartment_id = department['id']
                    break
        else:
            customerDepartment_id = ''
        
        
        #发送get_province api
        url = url = apis["get_province"]['url']
        response = call_api.get(url, self.token)
        for province in response["data"]:
            if province['name'] == recipient_province:
                province_id = province["id"]
                break
        
        
        #发送get_city api
        url = apis["get_city"]['url'] % (province_id)
        response = call_api.get(url, self.token)
        for city in response['data']:
            if city['name'] == recipient_city:
                city_id = city['id']
                break
        
    
        #发送get_country api
        url = apis["get_country"]['url'] % (city_id)
        response = call_api.get(url, self.token)
        for country in response['data']:
            if country['name'] == recipient_county:
                country_id = country['id']
                break
            
        
        #发送get_staff api
        if staff != '':
            url = apis["get_staff"]['url']
            body = json.dumps(apis["get_staff"]['body'], ensure_ascii=False) % (staff)
            response = call_api.post(url, body, self.token)
            staff_id = response["data"][0]["id"]
            print("====================================================if=")
        else:
            print("====================================================else")
            print("self.user_id:   " + str(self.user_id))
            staff_id = self.user_id
            print("staff_id:     " + str(staff_id))
            
        
        
        #发送get_bizStaff api
        if biz_staff != '':
            url = apis["get_bizStaff"]['url']
            body = json.dumps(apis["get_bizStaff"]['body'], ensure_ascii=False) % (self.organization_id,biz_staff)
            response = call_api.post(url, body, self.token)
            biz_staff_id = response["data"][0]["id"]
        else:
            biz_staff_id = self.user_id
        
        
        #发送get_warehouse api
        url = apis["get_warehouse"]['url']
        response = call_api.get(url, self.token)
        for ware_house in response['data']:
            if ware_house['name'] == warehouse:
                warehouse_id = ware_house["id"]
                break
    
        #发送get_sku api
        url = apis["get_sku"]['url']
        itemList = []
        for sku_no in sku_nos:  
            print(sku_no)
            body = json.dumps(apis["get_sku"]['body'], ensure_ascii=False) % (warehouse_id, sku_no)
            response = call_api.post(url, body, self.token)
            
            itemQty = 5;
            currentDiscount = 100;
            currentPrice = response["data"][0]['websitePrice'] * float(currentDiscount) * 0.01;
            amount = itemQty * float(currentPrice);
            
            sku = {
                "serverId": "",
                "skuName": response["data"][0]['skuName'],
                "currentDiscount": "100.00",
                "currentPrice": str(currentPrice),
                "itemMemo": "商品备注_" + sku_no,
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
        url = apis["submit_order"]['url']
        
        urgents = urgent==1
        expectedDeliveryDate = date(date.today().year, date.today().month, date.today().day + 1)
        expectedDeliveryDate = str(expectedDeliveryDate)
        body = {'itemList': itemList,
                'customerId': customer_id,  # 客户id
                'customerUserGroupId': customerDepartment_id,  # 客户用户组id(customerDepartment的id)
                'customerUserId': '',  # 客户采购人id（user表id）
                'deliveryMemo': '',  # 发货备注，永远是空
                'expectedDeliveryDate': expectedDeliveryDate,  # 期望配送日期
                'orderMemo': order_memo,  # 订单备注
                'orderType': order_type,  # 业务类型（0：常规单，1：赠品单，2：积分单）
                'packageMemo': '',  # XXXX备注
                'packageType': '',  # XXXX类型
                'projectId': project_id,
                'receiveType': '',  # 目前设置为空
                'recipientAddressProvinceId': province_id,  # 地址-省
                'recipientAddressCityId': city_id,  # 地址-市
                'recipientAddressCountyId': country_id,  # 地址-区
                'recipientAddressLine': recipient_line,  # 地址-详细
                'recipientName': recipient_name,  # 收货人
                'recipientPhone': recipient_phone,  # 收货人电话
                'staffId': staff_id,  # 业务员id
                'bizStaffId': biz_staff_id,  # 商务员id
                'urgents': urgents,  # 是否紧急（false：否，true：是）
                'urgent': urgent,  # 是否紧急（0：否，1：是）
                'orderVisibleAtFront': 0,
                'memoOrderNo': memo_order_no,  # 备注订单号
                'serverId': self.organization_id  
                }
        response = call_api.post(url, json.dumps(body), self.token)
        order_no = response['data']
        return order_no
    



login_with_ui.get_user_info()
with open('./configuration/user_info.json', 'r+') as f:
            user_info = json.loads(f.read())
            print(user_info)
            token = user_info['token']
            user_id = user_info['user_id']
            organization_id = user_info['organization_id']

order = Order(token, user_id, organization_id, './cases/common/create_order.json')
order_no = order.create_order(project='测试CHY', customer='测试CHY-央企', warehouse= '曹红玉', sku_nos=['10066773'])
print(order_no)