import os
import jpype
import requests

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuration import environment_exection


# 发送erpweb api获取key、publicKey
def get_keys():
    erp_url = environment_exection.server_url + "/api/authorization-server/login/key/erpWeb"
    erp_headers = {'Accept': 'application/json, text/plain, */*'}

    try:
        response = requests.get(erp_url, erp_headers)
        print(response.json())
    except Exception as e:
        print(e)

    key = response.json()['data']['key']
    public_key = response.json()['data']['publicKey']
    private_key = key + environment_exection.server_password
    print("密码：===========" + environment_exection.server_password)
    return key, public_key, private_key


# 密码加密
def encrypt_password(public_key, private_key):
    jvm_path = jpype.getDefaultJVMPath()  # 获取jvm默认路径
    jar_path = './jars/leading-encrypt-1.0.2-SNAPSHOT-jar-with-dependencies.jar'

    jpype.startJVM(jvm_path, "-ea", f"-Djava.class.path={jar_path}")  # 启动jvm虚拟机，加载加密算法的jar包
    JClass = jpype.JClass('com.leading.encrypt.sm.SM2Utils')
    jc = JClass()
    password_encrypt = str(jc.encryptHex(public_key, private_key))
    jpype.shutdownJVM()
    return password_encrypt


# 发送token api获取Authorization
def get_token():
    key, public_key, private_key = get_keys()
    password_encrypt = encrypt_password(public_key, private_key)

    # 发送token api，获取权限
    token_url = environment_exection.server_url + "/api/authorization-server/oauth/token"
    print("token_url:========" + token_url)
    data = 'grant_type=password&username=' + environment_exection.server_username +'&password=' + password_encrypt
    print(data)
    token_headers = {'Accept': 'application/json, text/plain, */*',
                     'Authorization': 'Basic V0VCQVBQOldFQkFQUA==',
                     'Content-Type': 'application/x-www-form-urlencoded',
                     'key': key
                     }
    try:
        response = requests.post(token_url, data, headers=token_headers)
        print(response.json())
    except Exception as e:
        print(e)

    token = response.json()['token_type'] + ' ' + response.json()['access_token']
    return token

token = get_token()
print(token)