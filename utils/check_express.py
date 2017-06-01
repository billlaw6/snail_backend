# -*- encoding: utf-8 -*-
import urllib.request
import json

def check_express(company, code):
    """
    使用快递100公司的服务查询快递状态
    """
    url = "http://www.kuaidi100.com/query?type=%s&postid=%s" % (company, code)
    page = urllib.request.urlopen(url) #打开链接，请求快递数据
    content = page.read().decode("utf8")
    print(content)
    jsonObj = json.loads(content)
    print("当前状态：" + jsonObj.get("message") + "\n")

    status = jsonObj.get("status")
    if status == "200":
        for x in jsonObj.get("data"):
            print("%s %s" % (x.get("time"), x.get("context")))
            for key,value in x.items():
                print(key + ":" + value)

if __name__ == "__main__":
    """
    测试参数：huitongkuaidi，310016459585
    """
    # check_express("shunfeng","102290224058")
    check_express("huitongkuaidi","310016459585")
