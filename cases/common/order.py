from datetime import date, datetime
import json
import sys
import os
import time

from requests_toolbelt import MultipartEncoder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import call_api

class Order:
    
    def __init__(self, token, user_id, organization_id, real_name, mobile) :
        self.token = token
        self.user_id = user_id
        self.organization_id = organization_id
        self.real_name = real_name
        self.mobile = mobile
        
    
    def create_order(self, project, customer, warehouse, skus, customer_department='', staff = '', biz_staff='',
                    recipient_name='chy', recipient_phone='123456', recipient_province='北京市', recipient_city='北京市', recipient_county='朝阳区', 
                    recipient_line='大羊坊路新华国际广场', order_type=0, memo_order_no='', urgent=0, order_memo=''):
        '''  
        创建订单
        =======================
        
        必填项：\n
        project：项目\n
        customer：客户\n
        warehouse：仓库名称\n
        skus：商品编号,list类型,举例：[{"no":"12121", "num":1}]\n
        =======================================
        
        非必填项：\n
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
        with open(file='./cases/common/order.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
            

        #发送get_project api 
        url = apis[0]["get_project"]['url']
        body = json.dumps(apis[0]["get_project"]['body'], ensure_ascii=False) % (project)
        response = call_api.post(url, body, self.token)
        project_id = response["data"][0]["id"]
            
            
        #发送get_customer api
        url = apis[0]["get_customer"]['url']
        body = json.dumps(apis[0]["get_customer"]['body'], ensure_ascii=False) % (customer, project_id)
        response = call_api.post(url, body, self.token)
        customer_id = response["data"][0]["id"]

        
        #发送get_customerDepartment api
        if customer_department != '':
            url = apis[0]["get_customer"]['url'] % (customer_id)
            response = call_api.get(url, self.token)
            for department in response['data']:
                if department['name'] == customer_department:
                    customerDepartment_id = department['id']
                    break
        else:
            customerDepartment_id = ''
        
        
        #发送get_province api
        url = apis[0]["get_province"]['url']
        response = call_api.get(url, self.token)
        for province in response["data"]:
            if province['name'] == recipient_province:
                province_id = province["id"]
                break
        
        
        #发送get_city api
        url = apis[0]["get_city"]['url'] % (province_id)
        response = call_api.get(url, self.token)
        for city in response['data']:
            if city['name'] == recipient_city:
                city_id = city['id']
                break
        
    
        #发送get_country api
        url = apis[0]["get_country"]['url'] % (city_id)
        response = call_api.get(url, self.token)
        for country in response['data']:
            if country['name'] == recipient_county:
                country_id = country['id']
                break
            
        
        #发送get_staff api
        if staff != '':
            url = apis[0]["get_staff"]['url']
            body = json.dumps(apis[0]["get_staff"]['body'], ensure_ascii=False) % (staff)
            response = call_api.post(url, body, self.token)
            staff_id = response["data"][0]["id"]
        else:
            staff_id = self.user_id
            
        
        
        #发送get_bizStaff api
        if biz_staff != '':
            url = apis[0]["get_bizStaff"]['url']
            body = json.dumps(apis[0]["get_bizStaff"]['body'], ensure_ascii=False) % (self.organization_id,biz_staff)
            response = call_api.post(url, body, self.token)
            biz_staff_id = response["data"][0]["id"]
        else:
            biz_staff_id = self.user_id
        
        
        #发送get_warehouse api
        url = apis[0]["get_warehouse"]['url']
        response = call_api.get(url, self.token)
        for ware_house in response['data']:
            if ware_house['name'] == warehouse:
                warehouse_id = ware_house["id"]
                break
    
        #发送get_sku api
        url = apis[0]["get_sku"]['url']
        itemList = []
        for sku in skus:  
            body = json.dumps(apis[0]["get_sku"]['body'], ensure_ascii=False) % (warehouse_id, sku['no'])
            response = call_api.post(url, body, self.token)
            
            itemQty = sku['num'];
            currentDiscount = 100;
            currentPrice = response["data"][0]['websitePrice'] * float(currentDiscount) * 0.01;
            amount = itemQty * float(currentPrice);
            
            sku = {
                "serverId": "",
                "skuName": response["data"][0]['skuName'],
                "currentDiscount": "100.00",
                "currentPrice": str(currentPrice),
                "itemMemo": "商品备注_" + sku['no'],
                "itemQty": itemQty,
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
        url = apis[0]["submit_order"]['url']
        
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
    
    def generate_delivery(self, order_no, warehouse, delivery_sku, inStore_type=0, auto_invoice=0, invoice_type=0, need_post=0, need_receipt=0, tax_sign=0):
        '''
        生成发货单
        ==================
        
        必填项：\n
        order_no：销售单号\n
        warehouse: 仓库名称\n
        delivery_sku：发货商品，list类型 [{"no":"12121", "num":1}]\n
        =======================================
        
        非必填项：\n
        inStore_type: 入仓类型（0：入仓，1：厂直，2：特配），默认值：0\n
        auto_invoice：随单开票（0：否；1：是）， 默认值：0\n
        invoice_type：开票类型（0：专票，1：普票，2：电子发票），默认：0\n
        need_post：是否需要邮寄（0：不需要，1：需要）, 默认值0\n
        need_receipt：是否需要收据（0：不需要，1：需要）, 默认值0\n
        tax_sign：含税标志（0：不含税，1：含税）, 默认值0\n
        
        urgent：是否紧急同订单相同\n
        deliveryMemo：发货备注，取自订单备注\n
        '''
        
        #打开json文件
        with open(file='./cases/common/order.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
            
        
        #发送get_orderId api 
        url = apis[1]["get_orderId"]['url']
        body = json.dumps(apis[1]["get_orderId"]['body'], ensure_ascii=False) % (order_no)
        response = call_api.post(url, body, self.token)
        order_id = response["data"]['items'][0]["orderId"]
        
        
        #发送get_warehouse api
        url = apis[1]["get_warehouse"]['url']
        response = call_api.get(url, self.token)
        for ware_house in response['data']:
            if ware_house['name'] == warehouse:
                warehouse_id = ware_house["id"]
                break 
            
        
        #发票get_deliveryInfo api
        url = apis[1]["get_deliveryInfo"]['url'] % (order_id)
        response = call_api.get(url, self.token)
        customerUserGroupName = response['data']['customerUserGroupName']
        customerUserGroupId = response['data']['customerUserGroupId']
        customerUserGroupCode = response['data']['customerUserGroupCode']
        customerUserId = response['data']['customerUserId']
        
        orderType = response['data']['orderType']
        orderTypeText = response['data']['orderTypeText']
        documentType = response['data']['documentType']
        documentTypeText = response['data']['documentTypeText']
        
        projectName = response['data']['projectName']
        projectId = response['data']['projectId']
        customerName = response['data']['customerName']
        customerType = response['data']['customerType']
        customerId = response['data']['customerId']
        customerUserName = response['data']['customerUserName']
        
        recipientPhone = response['data']['recipientPhone']
        recipientAddressProvinceName = response['data']['recipientAddressProvinceName']
        recipientAddressCityName = response['data']['recipientAddressCityName']
        recipientAddressCountyName = response['data']['recipientAddressCountyName']
        recipientAddressLine = response['data']['recipientAddressLine']
        recipientAddressProvinceId = response['data']['recipientAddressProvinceId']
        recipientAddressCityId = response['data']['recipientAddressCityId']
        recipientAddressCountyId = response['data']['recipientAddressCountyId']
        expectedDeliveryDate = response['data']['expectedDeliveryDate']
        
        
        bizStaffName = response['data']['bizStaffName']
        bizStaffId = response['data']['bizStaffId']
        staffName = response['data']['staffName']
        staffId = response['data']['staffId']
        recipientName = response['data']['recipientName']
        
        urgent = response['data']['urgent']
        deliveryMemo = response['data']['deliveryMemo']
        
        orderDeliveryAmount = response['data']['orderDeliveryAmount']
        usableAmount = response['data']['usableAmount']
        returnAmount = response['data']['returnAmount']
        amount = response['data']['amount']
        list = response['data']['list']
        
        version = response['data']['version']
        memoOrderNo = response['data']['memoOrderNo']
        createTime = response['data']['createTime']
        useLeadingWMS = response['data']['useLeadingWMS']
        customerOrderNo = response['data']['customerOrderNo']
        
        
        
        #发送get_invoice api
        url = apis[1]["get_invoice"]['url'] % (customerId)
        response = call_api.get(url, self.token)
        for invoice in response['data']:
            if invoice_type == 0 and invoice["type"]==0 and invoice['status']==0: #纸质专票、且启用状态
                customerInvoiceId = invoice['id']
                invoiceTitleId = invoice['id']
                accountNo = invoice['accountNo']
                addressOnInvoice = invoice['addressOnInvoice']
                bank = invoice['bank']
                invoiceTitle = invoice["invoiceTitle"]
                phoneOnInvoice = invoice['phoneOnInvoice']  
                socialCreditCode = invoice['socialCreditCode']
                break
                
            elif (invoice_type ==1 or invoice_type ==2) and invoice["type"]==1 and invoice['status']==0: #纸质普票、且启用状态
                customerInvoiceId = invoice['id']
                invoiceTitleId = invoice['id']
                accountNo = invoice['accountNo']
                addressOnInvoice = invoice['addressOnInvoice']
                bank = invoice['bank']
                invoiceTitle = invoice["invoiceTitle"]
                phoneOnInvoice = invoice['phoneOnInvoice']
                socialCreditCode = invoice['socialCreditCode']
                break
            
        
        #拼接invoiceInfo
        if (invoice_type==0 or invoice_type==1) and need_post==1:
            receiverAddressCityId = 2
            receiverAddressCountyId = 3
            receiverAddressProvinceId = 4
            receiverAddressLine = '收票人详细地址'
            receiverName = "Judy-receiverName"
            receiverPhone = "123456-receiverPhone"
        else:
            receiverAddressCityId = ''
            receiverAddressCountyId = ''
            receiverAddressProvinceId = ''
            receiverAddressLine = ''
            receiverName = ""
            receiverPhone = ""
            
        if invoice_type ==2:
            invoiceEmail = 'judy@q.com'
        else:
            invoiceEmail = ''
            
        if auto_invoice==1:
            invoiceInfo = {
                "invoiceTitleId": invoiceTitleId,
                "accountNo": accountNo,
                "addressOnInvoice": addressOnInvoice,
                "bank": bank,
                "invoiceEmail": invoiceEmail,
                "invoiceTitle": invoiceTitle,
                "invoiceType": invoice_type,
                "needPost": need_post,
                "needReceipt": need_receipt,
                "phoneOnInvoice": phoneOnInvoice,
                "projectId": projectId,
                "receiverAddressCityId": receiverAddressCityId,
                "receiverAddressCountyId": receiverAddressCountyId,
                "receiverAddressProvinceId": receiverAddressProvinceId,
                "receiverName": receiverName,
                "receiverPhone": receiverPhone,
                "recipientAddressLine": receiverAddressLine,
                "socialCreditCode": socialCreditCode,
                "taxSign": tax_sign,
                "getSendData": ""
            }
        else:
            invoiceInfo={}
        
        
        #拼接generate_delivery接口body
        sdSupplierId = ""#特配供应商id
        sdSupplierName = ""#特配供应商name
        sdFeeRate = ""#特配费率
        specialInvoiceType=0#特配发票类型（0：专用发票；1：普通发票；9：无票；）
        
        orderDeliveryItemParamList = []
        index=0
        for sku in delivery_sku:
            sku_no = sku["no"]
            sku_num = sku["num"]
            
            for sku_o in list:
                if str(sku_o['skuNo']) == sku_no:
                    amount = sku_num * float(sku_o["orderPrice"])
                    taxRate = float(sku_o["taxRate"]) * 100
                    
                    sdAmount = "0.00"#特配小计
                    sdPrice = "0.0000"#特配单价
                    
                    item = {
                        "itemQty": sku_num,
                        "itemMemo": sku_o["itemMemo"],
                        "amount": amount,
                        "oldErpSkuId": sku_o["oldErpSkuId"],
                        "currentPrice": sku_o["currentPrice"],
                        "availableItemQty": sku_o["availableItemQty"],
                        "skuName": sku_o["skuName"],
                        "taxRate": taxRate,
                        "unit": sku_o["unit"],
                        "skuModel": sku_o["skuModel"],
                        "usedItemQty": sku_o["usedItemQty"],
                        "skuNo": sku_no,
                        "orderPrice": sku_o["orderPrice"],
                        "oldErpSkuName": sku_o["oldErpSkuName"],
                        "skuId": sku_o["skuId"],
                        "buyQty": sku_o["itemQty"],
                        "deliverQty": sku_o["availableItemQty"],
                        "stock": "--",
                        "cost": "--",
                        "sdAmount": sdAmount,
                        "sdPrice": sdPrice,
                        "selectList": [
                            {
                                "skuId": sku_o["skuId"],
                                "skuName": sku_o["skuName"]
                            }
			            ],
			            "index": index
                    }
                    orderDeliveryItemParamList.append(item)
            index +=1
        
        
        body={
            "autoInvoice": auto_invoice,
            "amount": amount,
            "bizStaffId": bizStaffId,
            "bizStaffName": bizStaffName,
            "customerUserId": customerUserId,
            "customerUserName": customerUserName,
            "customerUserGroupId": customerUserGroupId,
            "customerUserGroupName": customerUserGroupName,
            "customerUserGroupCode": customerUserGroupCode,
            "customerType": customerType,
            "customerId": customerId,
            "customerName": customerName,
            "customerInvoiceId": customerInvoiceId,
            "customerOrderNo": customerOrderNo,
            "customerReceiptAddress": recipientAddressProvinceName + "-" + recipientAddressCityName + "-" + recipientAddressCountyName + "-" + recipientAddressLine,
            "createTime": createTime,
            "deliveryMemo": deliveryMemo,
            "deliveryType": 2,
            "documentTypeText": documentTypeText,
            "documentType": documentType,
            "expectedDeliveryDate": expectedDeliveryDate,
            "invoiceInfo": invoiceInfo,
            "id": order_id,
            "inStoreType": inStore_type,
            "list": orderDeliveryItemParamList,
            "memoOrderNo": memoOrderNo,
            "no": order_no,
            "orderDeliveryItemParamList": orderDeliveryItemParamList,
            "orderId": order_id,
            "orderType": orderType,
            "orderTypeText": orderTypeText,
            "orderDeliveryAmount": orderDeliveryAmount,
            "projectName": projectName,
            "projectId": projectId,
            "recipientAddressProvinceId": recipientAddressProvinceId,
            "recipientAddressProvinceName": recipientAddressProvinceName,
            "recipientAddressCityId": recipientAddressCityId,
            "recipientAddressCountyName": recipientAddressCountyName,
            "recipientAddressCountyId": recipientAddressCountyId,
            "recipientAddressCityName": recipientAddressCityName,
            "recipientAddressLine": recipientAddressLine,
            "recipientName": recipientName,
            "recipientPhone": recipientPhone,
            "returnAmount": returnAmount,
            "sdSupplierId": sdSupplierId,
            "sdSupplierName": sdSupplierName,
            "sdFeeRate": sdFeeRate,
            "staffId": staffId,
            "staffName": staffName,
            "specialInvoiceType": specialInvoiceType,
            "urgent": urgent,
            "usableAmount": usableAmount,
            "useLeadingWMS": useLeadingWMS,
            "version": version,
            "warehouseId": warehouse_id,
        }
        # print()
        
        #发送generate_delivery api，生成发货单
        url = apis[1]["generate_delivery"]['url']
        body = json.dumps(body, ensure_ascii=False)
        response = call_api.post(url, body, self.token)
        delivery_id = response["data"]
        
        #发送get_deliveryNo api, 获取发货单号
        url = apis[1]["get_deliveryNo"]['url']
        body = json.dumps(apis[1]["get_deliveryNo"]['body'], ensure_ascii=False) % (order_no)
        response = call_api.post(url, body, self.token)
        delivery_no=''
        for delivery in response['data']['items']:
            if delivery['orderDeliveryId'] == delivery_id:
                delivery_no = delivery['orderDeliveryNo']
                break
        
        
        return delivery_no, delivery_id
    
    def out_warehouse(self, delivery_no):
        '''
        发货单出库
        ================
        
        必填项：\n
        delivery_no：来源单号(发货单号)
        '''
        
        #打开json文件
        with open(file='./cases/common/order.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
        
        #推送到仓库，发送：push_wms api
        url = apis[2]["push_wms"]['url']
        call_api.post(url, '', self.token)
        
        #发送：get_lockId api，获取锁库单信息
        url = apis[2]["get_lockId"]['url']
        body = json.dumps(apis[2]["get_lockId"]['body'], ensure_ascii=False) % (delivery_no)
        response = call_api.post(url, body, self.token)
        lock_id = response['data']['items'][0]['id']
        sourceOrderId = response['data']['items'][0]['sourceOrderId']
        sourceOrderNo = response['data']['items'][0]['sourceOrderNo']
        sourceOrderType = response['data']['items'][0]['sourceOrderType']
        
        #发送：manual_lock api，手动锁库
        url = apis[2]["manual_lock"]['url']
        body = json.dumps(apis[2]["manual_lock"]['body'], ensure_ascii=False) % (lock_id, sourceOrderId, sourceOrderNo, sourceOrderType)
        call_api.post(url, body, self.token)
        
        #发送：get_allocationId api，获取分配任务单信息
        url = apis[2]["get_allocationId"]['url']
        body = json.dumps(apis[2]["get_allocationId"]['body'], ensure_ascii=False) % (delivery_no)
        response = call_api.post(url, body, self.token)
        allocation_id = response['data']['items'][0]['id']
        
        #发送：allocate_picker_info api，获取分配人员信息
        url = apis[2]["allocate_picker_info"]['url']
        body = json.dumps(apis[2]["allocate_picker_info"]['body'], ensure_ascii=False) % (allocation_id)
        response = call_api.post(url, body, self.token)
        pickerId = response['data']['pickerStatisticInfoDTOList'][0]['pickerId']
        
        #发送：allocate_picker api，分配任务
        url = apis[2]["allocate_picker"]['url']
        body = json.dumps(apis[2]["allocate_picker"]['body'], ensure_ascii=False) % (allocation_id, pickerId)
        call_api.post(url, body, self.token)
        
        #发送：out_warehouse api，出库
        url = apis[2]["out_warehouse"]['url']
        body = json.dumps(apis[2]["out_warehouse"]['body'], ensure_ascii=False) % (self.user_id, self.real_name, self.mobile, sourceOrderId, sourceOrderNo)
        call_api.post(url, body, self.token)
        
        time.sleep(10)
    
    def confirmed_delivery(self, delivery_id):
        '''
        发货单确认送达
        ===============
        
        必填项：\n
        delivery_id：发货单加密id
        '''
        
        #打开json文件
        with open(file='./cases/common/order.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
        
        #发送: get_deliveryItemId api
        url = apis[3]["get_deliveryItemId"]['url'] % (delivery_id)
        response = call_api.get(url, self.token)
        receiveQtyDTOS = []
        for item in response['data']['orderDeliveryItemDTOS']:
            item = {
                "itemId": item["id"],
                "receiveQty":item["itemQty"]
            }
            receiveQtyDTOS.append(item)
            
        # 发送：upload_image api，上传图片
        image = ("upload.png", open("./cases/common/upload.png", 'rb'))
        url = apis[3]["upload_image"]['url']
        body = MultipartEncoder({
                "type": "Order_Document",
                "fileName": image
            })
        response = call_api.post_Image(url, body, self.token)
        upload_id = response["data"]["id"]
        
          
        #发送：confirmed_delivery，确认送达
        url = apis[3]["confirmed_delivery"]['url']
        now = datetime.today()
        now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        body = {
            "cargoReceiptPictureFileIds": [upload_id],
            "deliveryTime": str(now),
            "id": delivery_id,
            "receiveQtyDTOS": receiveQtyDTOS
        }
        body=json.dumps(body, ensure_ascii=False)
        response = call_api.put(url, body, self.token)
        
    def return_order(self, delivery_no, delivery_id, return_sku):
        '''
        退货完成
        ======================
        
        必填项：\n
        delivery_no：发货单号\n
        delivery_id：发货单加密id\n
        return_sku：退货商品, list, 举例: [{"no": "101111", num":1}]\n
        '''    
        
         #打开json文件
        with open(file='./cases/common/order.json', mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
        
        #发送：returnOrder_contactInfo api，获取退货联系信息
        url = apis[4]["returnOrder_contactInfo"]['url'] % (delivery_id)
        response = call_api.get(url, self.token)
        returnAddressCityId = response['data']['returnAddressCityId']
        returnAddressCountyId = response['data']['returnAddressCountyId']
        returnAddressLine = response['data']['returnAddressLine']
        returnAddressProvinceId = response['data']['returnAddressProvinceId']
        returnContacts = response['data']['returnContacts']
        returnPhone = response['data']['returnPhone']
        returnReasons = response['data']['returnReasons']
        warehouseId = response['data']['warehouseId']
        warehouseName = response['data']['warehouseName']
        
        #发送returnOrder_SkuItemList api，获取退货商品信息
        url = apis[4]["returnOrder_SkuItemList"]['url'] 
        body = json.dumps(apis[4]["returnOrder_SkuItemList"]['body']) % (delivery_id)
        response = call_api.post(url, body, self.token)
        
        returnOrderWarehouseItemParamList=[]
        for sku in return_sku:
            for data in response['data']:
                if sku['no'] == str(data['skuNo']):
                    item={
                        "actualReturnQty": data['canReturnNum'],
                        "canReturnNum": data['canReturnNum'],
                        "currentPrice":data['currentPrice'],
                        "id":data['id'],
                        "orderDeliveryId":data['orderDeliveryId'],
                        "orderDeliveryItemId":data['id'],
                        "returnQty":sku['num'],
                        "sdAmount":data['sdAmount'],
                        "skuId":data['skuId'],
                        "skuModel":data['skuModel'],
                        "skuName":data['skuName'],
                        "skuNo":data['skuNo'],
                        "taxRate":data['taxRate'],
                        "unit":data['unit']
                    }
                    returnOrderWarehouseItemParamList.append(item)
                    
        #发送generate_returnOrder api，生成退货单
        url = apis[4]["generate_returnOrder"]['url'] % (delivery_id)
        body = {
            "orderType": 0,
            "otherReasonDescription": "",
            "receiver":"",
            "receiverAddressCityId":"",
            "receiverAddressCountyId":"",
            "receiverAddressLine": "",
            "receiverAddressProvinceId":"",
            "receiverPhone":"",
            "returnAddressCityId": returnAddressCityId,
            "returnAddressCountyId": returnAddressCountyId,
            "returnAddressLine": returnAddressLine,
            "returnAddressProvinceId": returnAddressProvinceId,
            "returnContacts": returnContacts,
            "returnOrderWarehouseItemParamList": returnOrderWarehouseItemParamList,
            "returnPhone": returnPhone,
            "returnReason": "ORDER_INFO_ERROR",#[ ORDER_INFO_ERROR, CUSTOMER_CHANGE_SKU, OUT_OF_CUSTOMER_MONEY, CUSTOMER_NEED_CHANGE, OTHER ]
            "returnReasons": returnReasons,
            "returnWay": "RETURN_WAREHOUSE", #[ RETURN_FACTORY, RETURN_WAREHOUSE ]
            "status": 2,
            "warehouseId": warehouseId,
            "warehouseName": warehouseName
        }
        response = call_api.post(url, json.dumps(body, ensure_ascii=False), self.token)
        
        #发送get_returnOrderInfo api，获取退货单信息
        url = apis[4]["get_returnOrderInfo"]['url'] 
        body = json.dumps(apis[4]["get_returnOrderInfo"]['body']) % (delivery_no)
        response = call_api.post(url, body, self.token)
        returnorder_no = response['data']['items'][0]['returnOrderNo']
        returnorder_id = response['data']['items'][0]['id']
            
        #发送confirm_returnOrder api,确认退货单
        url = apis[4]["confirm_returnOrder"]['url'] % (returnorder_id)
        body = json.dumps(apis[4]["confirm_returnOrder"]['body'])
        call_api.put(url, body, self.token)
            

        #发送warehouse_returnOrderInfo api，销售退货获取退货信息
        url = apis[4]["warehouse_returnOrderInfo"]['url'] 
        body = json.dumps(apis[4]["warehouse_returnOrderInfo"]['body']) % (returnorder_no)
        response = call_api.post(url, body, self.token)
        returnOrderItems = response['data']['items'][0]['returnOrderItems']
        for item in returnOrderItems:
            item['inQty'] = item['returnQty']
            item['warehouseId'] = warehouseId
            item['warehouseName'] = warehouseName
            if item['locationId'] == None:
                item['locationId'] = 0
            
        
        #发送returnOrder_inWarehouse api, 销售退货入库
        url = apis[4]["returnOrder_inWarehouse"]['url'] 
        body = json.dumps(returnOrderItems, ensure_ascii=False)
        call_api.post(url, body, self.token)
        
        return returnorder_no, returnorder_id