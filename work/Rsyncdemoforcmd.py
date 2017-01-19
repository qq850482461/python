import tkinter as tk
import os
import tkinter.messagebox
from tkinter.filedialog import askdirectory

class App():
    def __init__(self,root):
        self.root = root
        self.v1 = tk.StringVar()
        self.root.title("demo")
        self.root.geometry("263x65")
        self.root.resizable(False, False)#禁止改变窗口大小

    def selectPath(self):
        path = askdirectory()
        self.v1.set(path)

    def rsync(self,path,ip = "192.168.1.6",module = "backup",):
      path = str(path)
      ip = str(ip)
      module = str(module)

      cmd = "rsync -rlptgDzP --backup --suffix=_backup /cygdrive/{0} {1}::{2}".format(path,ip,module)

      if os.path.isdir("cwRsync"):
          os.chdir(r"cwRsync\bin")
      print('进入目录成功')
      shell = os.system(cmd)
      return shell

    def updata(self):
        path = self.v1.get()
        if len(path) == 0:
            tkinter.messagebox.showerror("提示", "上传目录不能为空")
        else:
            start_path = path[0:1]
            end_path = path[2:]
            path = str(start_path+end_path)
            print(os.getcwd())
            result = self.rsync(path)

            if result == 0:
                tkinter.messagebox.showinfo("提示", "上传完成")
            else:
                tkinter.messagebox.showerror("提示", "上传失败")

    def windows(self):
        tk.Label(self.root, text="目标路径:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.v1,state="readonly").grid(row=0, column=1)
        tk.Button(self.root, text="路径选择", command=self.selectPath).grid(row=0, column=2)
        tk.Button(self.root, text="上传目录",command=self.updata).grid(row=1,column=1)
        print("第一次同步文件量大需要耐心等待")


if __name__ == "__main__":

    root = tk.Tk()
    # tkinter窗口居中
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (263, 65, (screenwidth - 263) / 2, (screenheight - 65) / 2)
    root.geometry(size)

    app = App(root)
    app.windows()
    root.mainloop()

