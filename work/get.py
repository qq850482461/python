import requests

"""""
params = {

    "key": "e569d23be8a46dfa265b6c647f023d3e",  # 应用APPKEY(应用详细页查询)
    "ip": "116.1.74.47",  # 需要查询的IP地址或域名
    "dtype": "json",  # 返回数据的格式,xml或json，默认json

}
res = requests.get('http://apis.juhe.cn/ip/ip2addr',params=params)
print(res.url)
json = res.json()
print(json)
"""""

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
res = requests.get("http://www.baidu.com",headers=headers)

res.encoding = "utf-8"
print(type(res.text))


