import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import send_api

def bill_list(token):
    response = send_api.sendApi("./all_apis/bill_apis.json", "Bill_list api", token)
    return response["message"]

def bill_delete(token):
    response = send_api.sendApi("./all_apis/bill_apis.json", "Bill_delete api", token)
    return response["message"]