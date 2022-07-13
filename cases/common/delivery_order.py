from datetime import date
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import call_api

class Delivery:
    
    def __init__(self, token, user_id, organization_id, data_path) :
        self.token = token
        self.user_id = user_id
        self.organization_id = organization_id
        self.data_path = data_path
        
        
    def generate_delivery(self, order_no, warehouse, delivery_sku, inStore_type=0, auto_invoice=0, invoice_type=0, need_post=0, need_receipt=0, tax_sign=0):
        '''
        必填项：
        ========================
        order_no：销售单号\n
        warehouse: 仓库名称\n
        delivery_sku：发货商品，list类型 [{"no":"12121", "num":1}]\n
        =======================================
        
        非必填项：
        ========================
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
        with open(file=self.data_path, mode="r", encoding="utf-8") as f:
            apis = json.loads(f.read())
            
        
        #发送get_orderId api 
        url = apis["get_orderId"]['url']
        body = json.dumps(apis["get_orderId"]['body'], ensure_ascii=False) % (order_no)
        response = call_api.post(url, body, self.token)
        order_id = response["data"]['items'][0]["orderId"]
        
        
        #发送get_warehouse api
        url = apis["get_warehouse"]['url']
        response = call_api.get(url, self.token)
        for ware_house in response['data']:
            if ware_house['name'] == warehouse:
                warehouse_id = ware_house["id"]
                break 
            
        
        #发票get_deliveryInfo api
        url = apis["get_deliveryInfo"]['url'] % (order_id)
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
        url = apis["get_invoice"]['url'] % (customerId)
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
        
        print("invoiceInfo=================================\n" + json.dumps(invoiceInfo, ensure_ascii=False))
        
        
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
        
        #发送generate_delivery api
        url = apis["generate_delivery"]['url']
        body = json.dumps(body, ensure_ascii=False)
        response = call_api.post(url, body, self.token)
        delivery_id = response["data"]
        
        return delivery_id
        
        