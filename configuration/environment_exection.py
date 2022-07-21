import json

#所有的测试环境
environments = ['./configuration/environment_test.json', 
                './configuration/environment_test1-2.json',
                './configuration/environment_test1-3.json',
                './configuration/environment_test2.json',
                './configuration/environment_test2-2.json',
                './configuration/environment_test2-3.json']


#设置执行环境
exection = "environment_test2"

#查找执行环境参数
for each in environments:
    if exection in each :
        with open(each,'r',encoding='utf8')as fp:
            json_data = json.load(fp)
            server_url = json_data['server']['url']
            server_username = json_data['server']['username']
            server_password = json_data['server']['password']
            database_host = json_data['database']['host']
            database_port = json_data['database']['port']
            database_username = json_data['database']['username']
            database_password = json_data['database']['password']
            database_finance = json_data['database']['database_finance']
            database_leading = json_data['database']['database_leading']
            database_user = json_data['database']['database_user']
        break
