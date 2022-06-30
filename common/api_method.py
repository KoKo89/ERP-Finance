import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuration import environment_exection


# post request
def post(url, body, token):
    global response
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token,
               'Content-Type': 'application/json;charset=UTF-8'}
    url = environment_exection.server + url
    data = body
    try:
        response = requests.post(url, data.encode('utf-8'), headers=headers)
        print(url + ': ' + response.json()['message'])
    except Exception as e:
        print(e)
    return response


def put(url, body, token):
    global response
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token,
               'Content-Type': 'application/json;charset=UTF-8'}
    url = environment_exection.server + url
    data = body
    try:
        response = requests.put(url, data.encode('utf-8'), headers=headers)
        print(url + ': ' + response.json()['message'])
    except Exception as e:
        print(e)
    return response


def get(url, token):
    global response
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token}
    url = environment_exection.server + url
    try:
        response = requests.get(url, headers=headers)
        print(url + ': ' + response.json()['message'])
    except Exception as e:
        print(e)
    return response


def delete(url, token):
    global response
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': token}
    url = environment_exection.server + url
    try:
        response = requests.delete(url, headers=headers)
        print(url + ': ' + response.json()['message'])
    except Exception as e:
        print(e)
    return response
