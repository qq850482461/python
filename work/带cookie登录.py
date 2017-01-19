import urllib.request
import urllib.parse
import http.cookiejar


class Lonin():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = "https://www.juhe.cn/login"
        self.posturl = "https://www.juhe.cn/login/login"

    def opener(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        data = {'username': self.username, 'password': self.password,"captcha":""}
        postdata = urllib.parse.urlencode(data).encode("utf-8")  # 编码data

        cookie_filename = "cookie.txt"
        cookie = http.cookiejar.MozillaCookieJar(cookie_filename)  # 创建cookie实例化
        handler = urllib.request.HTTPCookieProcessor(cookie)  # cookie处理器
        opener = urllib.request.build_opener(handler)  # 重构open带入cookie

        req = urllib.request.Request(url=self.posturl, data=postdata, headers=headers)
        res = opener.open(req)

        cookie.save(cookie_filename,ignore_discard=True, ignore_expires=True)

        get_req = urllib.request.Request(url=self.url,headers=headers)
        get_res = opener.open(get_req)
        html = get_res.read().decode("utf-8")
        return html


if __name__ =="__main__":
    login = Lonin("18593236586","mima123")
    html = login.opener()
    print(html)