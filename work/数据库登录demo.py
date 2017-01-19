import mysql.connector

conn = mysql.connector.connect(host = "192.168.1.55",
                               port = 3306,
                               user = "root",
                               password = "lzh3101977",
                               database="test"
                               )
cursor = conn.cursor()

class Loin(object):

    def join(self):
        check_username = True
        check_password = True
        while check_username:
            name = str(input("输入要注册的用户名："))
            sql = "select * from user where username = '{0}'".format(name)
            cursor.execute(sql)
            valeus = cursor.fetchall()
            print(valeus)
            if len(valeus)>=1:
                for i in valeus:
                    if name in i :
                        print("您输入的账户%s已被注册,请重新输入" % name)
            else:
                check_username = False
                print("您输入的帐号可以使用")
        username = name

        password1 = input("输入您的密码:")
        password2 = input("请再次输入您的密码:")
        while password2 != password1:
            print("您2次输入的密码不相同请重新输入:")
            password1 = input("输入您的密码:")
            password2 = input("请再次输入您的密码:")
        password = password2

        try:
            add_sql = "insert into user (username,password) values({0},{1})".format(username,password)
            cursor.execute(add_sql)
            conn.commit()
            print("注册成功")
        except:
            print("错误")
        finally:
            cursor.close()

    def loin(self):
        username = input("输入你的帐号：")
        password = input("输入你的密码：")
        find_sql = 'select * from user where username = "{0}" and password = "{1}"'.format(username,password)
        cursor.execute(find_sql)
        valeus = cursor.fetchall()
        print(valeus)
        if len(valeus) < 1:
            print("您输入的账户或者密码不正确")
        else:
            print("登录成功欢迎您:%s" % username)


if __name__ =="__main__":
    loin = Loin()
    loin.loin()
