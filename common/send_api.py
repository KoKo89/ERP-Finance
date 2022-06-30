import json
from common import api_method


def sendApi(filePath, apiName, token):
    #读取api Json文件
    with open(file=filePath, mode="r+", encoding="utf-8") as jsonFile:
        apis = json.loads(jsonFile.read())
    
    if apis[apiName]["method"] == "POST":
        response = api_method.post(apis[apiName]["url"], apis[apiName]["body"], token)
        
    elif apis[apiName]["method"] == "PUT":
        response = api_method.put(apis[apiName]["url"], apis[apiName]["body"], token)
        
    elif apis[apiName]["method"] == "GET":
        response = api_method.get(apis[apiName]["url"],token)
        
    elif apis[apiName]["method"] == "DELETE":
       response = api_method.get(apis[apiName]["url"],token)
       
    
    return response