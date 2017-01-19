import mysql
import mysql.connector.errors

conn = mysql.connector.connect(host = "127.0.0.1",
                               port = 3306,
                               user = "root",
                               password = "lzh3101977",
                               database = "test"
                               )
cursor = conn.cursor()

#cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
def add(id,name):
    id = id
    name = name
    try:
        cursor.execute('insert into user (id, name) values (%s, %s)', [id, name])
        conn.commit()
    except mysql.connector.errors.IntegrityError as e:
        print("提交ID重复error",e)
        conn.rollback()
    finally:
        print("成功提交")
        conn.close()
def find():
    sql = 'select * from user'
    cursor.execute(sql)
    values = cursor.fetchall()
    for i in values:
        print("ID = %s , NAME = %s" % i)
    conn.close()
    return values

def updata(id,name):
    id = id
    name = name

    try:
        cursor.execute('update user set name=%s where id=%s',(name,id))
        conn.commit()
    except mysql.connector.errors.IntegrityError as e:
        print("提交ID重复error", e)
        conn.rollback()
    finally:
        print("成功提交")
        conn.close()

def delete(id):
    id = id
    try:
        cursor.execute('delete from user where id=%s',(id,))
        conn.commit()
        print("成功提交")
    except mysql.connector.errors.IntegrityError as e:
        print("提交ID重复error", e)
        conn.rollback()
    finally:

        conn.close()

add("002","周周2")