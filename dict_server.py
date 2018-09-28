#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'''
电子词典服务端

项目名称：电子词典

相关技术：多进程，Mysql等

作者：焦鹏博

QQ:1164998066

邮箱：1164998066@qq.com

日期：2018-09-28

'''


from socket import *
import os
import pymysql
import signal
import sys
from time import sleep

#注册
def user_sql_zc(db,cur,c,name,passwd):
    cur = db.cursor()
    try:
        cur.execute("select name from user where name = '%s'" % name)
    except:
        c.send('对比数据库失败'.encode())
        print('对比数据库失败')
        db.close()
    else:
        data = cur.fetchall()
        if not data:
            try:
                # 将注册用户信息存入数据库
                cur.execute('insert into user (name,passwd) values("%s","%s")' % (name,passwd))
                db.commit()
            except:
                print('信息写入数据库失败')
                c.send('信息写入数据库失败'.encode())
                db.roolback()
                db.close()
                return
            c.send(b'OK')
        else:
            c.send(b'not ok')

#登录
def user_sql_dl(db,cur,c,name,passwd):
    try:
        # 判断用户名是否存在数据库
        cur.execute("select name,passwd from user where name = '%s'" % name)
    except:
        c.send('对比数据库失败'.encode())
        db.close()
    else:
        # 接受数据库返回的信息
        data = cur.fetchall()
        if not data:
            c.send(b'not ok')
            return
        if data[0][0] == name and data[0][1] == passwd:
            c.send(b'OK')
        else:
            c.send(b'not ok')

#查词
def cc(db,cur,c,word,dl_name):
    try:
        # 将查询单词和用户名存入数据库　并且查询该单词
        cur.execute('insert into hist(name,word) values("%s","%s")' % (dl_name,word))
        cur.execute('select *from words where word = "%s"' % word)
        data = cur.fetchall()
        if data:
            c.send(b'OK')
            sleep(0.1)
            c.send(data[0][2].encode())
        else:
            c.send(b'not ok')
        db.commit()
    except Exception as e:
        print(e)


#查历史记录
def ch(db,cur,c,dl_name):
    try:
        cur.execute('select name,word,time from hist where name = "%s"'% dl_name)
        data = cur.fetchall()
    except:
        c.send('查询异常'.encode())
    else:
        c.send(str(data).encode())



# 服务端主框架
def main():
    #连接数据库
    db = pymysql.connect('localhost','root','123456','dict')
    cur = db.cursor()
    # 创建套接字
    s = socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('0.0.0.0',8888))
    s.listen(5)

    #当子进程退出时忽略该信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while 1:
        try:
            c,addr = s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务端退出')
        else:
            # 创建多进程
            pid = os.fork()
            if pid == 0:
                s.close()
                print('子进程准备处理客户端请求')
                dl_name = ''
                while 1:
                    try:
                        data = c.recv(1024).decode()
                    except:
                        break
                    if not data:
                        break
                    # 服务端调用功能函数
                    if data.split(' ')[0] == 'ZC':
                        name = data.split(' ')[1]
                        passwd = data.split(' ')[2]
                        user_sql_zc(db,cur,c,name,passwd)
                    elif data.split(' ')[0] == 'DL':
                        name = data.split(' ')[1]
                        dl_name = name
                        passwd = data.split(' ')[2]
                        user_sql_dl(db,cur,c,name,passwd)
                    elif data.split(' ')[0] == 'CC':
                        word = data[3:]
                        cc(db,cur,c,word,dl_name)
                    elif data == 'CH':
                        ch(db,cur,c,dl_name)
                sys.exit(0)
            else:
                c.close()
               

if __name__ == '__main__':
    main()
                
