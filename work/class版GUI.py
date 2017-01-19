from tkinter import *
import urllib.request

class App():
    def __init__(self,root):
        self.root = root
        self.root.title("demo")
        self.root.geometry("400x300")
        self.text = None
        self.url = None
        #self.root.resizable(False, False)#禁止改变窗口大小


    def urlopen(self,url):
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0")
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        return html

    def print(self):
        url = self.url.get()
        print(type(url),url)
        #text = self.urlopen(url)
        v1.set("123")

    def windows(self):
        Label(self.root, text="url:").grid(row=0, column=0, sticky="w")
        self.url = Entry(self.root, width="30")  # .grid(row=0, column=1, padx=10, pady=5)
        self.url.grid(row=0, column=1, padx=10, pady=5)
        global v1
        v1 = StringVar
        self.text = Entry(self.root, textvariable=v1,width="30")
        self.text.grid(row=1, column=1, padx=10, pady=5)

        Button(self.root, text="分析", comman=self.print).grid(row=2, column=0, sticky="w")


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    app.windows()
    root.mainloop()