import urllib.request
import urllib.parse
import json

#定义一个content（内容）翻译的变量
content = input("输入翻译的内容：")

#修改head头
head = {}
head["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"

#url以对象的方式传入
url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=https://www.baidu.com/link"

#data表单是以字典传入
data = {}

data["type"] = "AUTO"
data["i"] = content
data["doctype"] = "json"
data["xmlVersion"] = "1.8"
data["keyfrom"] = "fanyi.web"
data["ue"] = "UTF-8"
data["action"] = "FY_BY_CLICKBUTTON"
data["typoResult"] = "true"

#进行把data字典urlencode编码转换成为utf-8的表单形式
data = urllib.parse.urlencode(data).encode("utf-8")

#发送一个get请求把head放进去
req = urllib.request.Request(url,data,head)

#urlopen函数填写上了url data（表单）就会将把get请求转换成post请求 (打开)
response = urllib.request.urlopen(req)

#进行读取并且转换成为了utf-8 (读取)
html = response.read().decode("utf-8")

#通过json转换得到的html内容成为字典
json.loads(html)
results = json.loads(html)

#因为访问字典key得到的value是一个列表再对列表进行格式化打印输出结果
print("翻译结果是：{:s}".format(results["translateResult"][0][0]["tgt"]))
