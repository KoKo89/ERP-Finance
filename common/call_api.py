import json
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuration import environment_exection


# post request
def post(url, body, token):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token,
               'Content-Type': 'application/json;charset=UTF-8'}
    url = environment_exection.server_url + url
    data = body
    
    try:
        response = requests.post(url, data.encode('utf-8'), headers=headers)
        print(url + ":")
        print(response.json())
        print("=========================================================================================\n")
        return response.json()
    except Exception as e:
        print(e)
   
   
def post_Image(url, body, token):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token,
               'Content-Type': body.content_type}
    url = environment_exection.server_url + url
    data = body
    
    try:
        response = requests.post(url, data, headers=headers)
        print(url + ":")
        print(response.json())
        print("=========================================================================================\n")
        return response.json()
    except Exception as e:
        print(e)


def put(url, body, token):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token,
               'Content-Type': 'application/json;charset=UTF-8'}
    url = environment_exection.server_url + url
    data = body
    
    try:
        response = requests.put(url, data.encode('utf-8'), headers=headers)
        print(url + ":")
        print(response.json())
        print("=========================================================================================\n")
        return response.json()
    except Exception as e:
        print(e)
   


def get(url, token):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token}
    url = environment_exection.server_url + url
    try:
        response = requests.get(url, headers=headers)
        print(url + ":")
        print(response.json())
        print("=========================================================================================\n")
        return response.json()
    except Exception as e:
        print(e)



def delete(url, token):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token}
    url = environment_exection.server_url + url
    
    try:
        response = requests.delete(url, headers=headers)
        print(url + ":")
        print(response.json())
        print("=========================================================================================\n")
        return response.json()
    except Exception as e:
        print(e)
