import urllib.request
import json

content = input("手机号：")

appkey = "7aed273b8a92aab7644a3c2eda3016b3"
url = "http://apis.juhe.cn/mobile/get"

params = {
    "phone": content,  # 需要查询的手机号码或手机号码前7位
    "key": appkey,  # 应用APPKEY(应用详细页查询)
    "dtype": "json",  # 返回数据的格式,xml或json，默认json
 }
params=urllib.parse.urlencode(params).encode("utf-8")
req = urllib.request.Request(url,params)
res = urllib.request.urlopen(req)
html = res.read().decode("utf-8")

json.loads(html)
results = json.loads(html)
result = results["result"]
print("手机号",content,
      "\n运营商：",result["company"],
      "\n归属地：",result["city"],
      "\n邮编：",result["zip"],
      "\n座机号：",result["areacode"],
      )