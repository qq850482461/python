import tkinter as tk
import tkinter.messagebox


root = tk.Tk()

tk.Label(root,text="帐号").grid(row=0,column=0)
tk.Label(root,text="密码").grid(row=1,column=0)

v1 = tk.StringVar()
v2 = tk.StringVar()

e1 = tk.Entry(root,textvariable=v1).grid(row=0,column=1,padx=10,pady=5)
e2 = tk.Entry(root,textvariable=v2,show="*").grid(row=1,column=1,padx=10,pady=5)



def name():
    if v1.get() == "123" and v2.get()== "123":
        tkinter.messagebox.showinfo("登录","登录成功恭喜")
    else:
        tkinter.messagebox.showwarning("错误","失败")
def windows():
    root = tk.Tk()
    frame = tk.Frame(root)
    tk.Label(frame, text="帐号").grid(row=0, column=0)
    tk.Label(frame, text="密码").grid(row=1, column=0)
    tk.Label(frame, text="确认密码").grid(row=2, column=0)

    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()

    e1 = tk.Entry(frame,textvariable=v1).grid(row=0,column=1,padx=10,pady=5)
    e2 = tk.Entry(frame, textvariable=v2,show="*").grid(row=1, column=1, padx=10, pady=5)
    e3 = tk.Entry(frame, textvariable=v3,show="*").grid(row=2, column=1, padx=10, pady=5)

    tk.Button(root,text="注册").grid(row=3,column=0,sticky="W",padx=10,pady=5)
    tk.Button(root, text="取消",comman=root.quit).grid(row=3,column=1,sticky="S",padx=10,pady=5)

tk.Button(root,text="登录",comman=name).grid(row=3,column=0,sticky="W",padx=10,pady=5)
tk.Button(root,text="注册",comman=windows).grid(row=3,column=1,sticky="S",padx=10,pady=5)


tk.mainloop()

