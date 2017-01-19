import bs4
import urllib.error
import urllib.request
import re
import os

def get_html(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36")
    res = urllib.request.urlopen(req)
    html = res.read()
    return html

def find_page(url):
    html = get_html(url).decode("utf-8")
    reg = r'href="(\?start=.+?=)"'
    page_list = re.findall(reg,html)
    del page_list[-1]
    del page_list[-1]
    all_list = ["https://movie.douban.com/top250?start=0&filter=",]
    prefix = "https://movie.douban.com/top250"
    for i in page_list:
        url = prefix + i
        all_list.append(url)
    return all_list


def folder(name="电影"):
    if os.path.isdir(name):
        os.chdir(name)
    else:
        print("正在创建",name)
        os.mkdir(name)
        os.chdir(name)

def get_synopsis(url):
    soup = bs4.BeautifulSoup(get_html(url).decode("utf-8"),"html.parser")
    str1 = soup.find("span", property="v:summary").get_text()
    return str(str1)


def save_txt(url):
    soup = bs4.BeautifulSoup(get_html(url).decode("utf-8"),"html.parser")
    for tag in soup.find_all("div", class_="item"):
        rating = tag.find("span", class_="rating_num").string  # 评分
        director = tag.find("p", class_="").get_text()  # 导演
        name = tag.find("span", class_="title").string  # 电影名称
        url = tag.find("a").get("href")  # 得到电影详细url
        try:
            synopsis = get_synopsis(url) #得到电影每一个url内部的简介
        except:
            print("错误")

        with open(str(name) + ".txt", "w", encoding='utf-8') as f:
            print("正在保存", str(name))
            f.write(str(name) + "\n")
            f.write(director.strip() + "\n")
            f.write(synopsis.strip() + "\n")
            f.write("评分" + str(rating) + "\n")
            f.write("网址" + str(url))


if __name__ == "__main__":
    url = "https://movie.douban.com/top250?start="
    folder()
    for i in find_page(url):
        save_txt(i)