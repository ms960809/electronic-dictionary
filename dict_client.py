#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'''
电子词典客户端

项目名称：电子词典

相关技术：多进程，Mysql等

作者：焦鹏博

QQ:1164998066

邮箱：1164998066@qq.com

日期：2018-09-28

'''

from socket import *
import sys
from time import sleep

#注册
def zc(s):
    while 1:
        name = input('name>>') or'0'
        if name == '0':
            break
        passwd = input('passwd>>')
        s.send(('ZC '+name+' '+passwd).encode())
        data = s.recv(1024)
        if data == b'OK':
            print('成功注册账号!!')
            return
        else:
            print('账号已存在!!!')

#查询
def cx(s):
    while 1:
        print('''+---------------------------------+
|  1.查单词  2.历史记录   3.退出     |
+----------------------------------+
            ''')
        n = input('请输入选择>>')
        if n == '1':
            while 1:
                word = input('请输入要查找的单词>>')
                if word == '##':
                    break
                s.send(('CC '+word).encode())
                data = s.recv(1024)
                if data == b'OK':
                    d = s.recv(1024)
                    print(d.decode())
                else:
                    print('没有该单词')
        elif n == '2':
            s.send(b'CH')
            data = s.recv(1024).decode()
            if data == 'not ok':
                print('没有记录!!!')
            elif data == '查询异常':
                print(data)
            else:
                l = data.split(',')
                print(l)


        elif n == '3':
            return
        else:
            print('请输入正确选项')
            sys.stdin.flush()#清楚标准输入
            continue

#登录
def dl(s):
    while 1:
        name = input('name>>')
        passwd = input('passwd>>')
        s.send(('DL '+name+' '+passwd).encode())
        data = s.recv(1024)
        if data == b'OK':
            print('成功登录账号!!')
            cx(s)
            break
        else:
            print('账号或密码错误!!!')


def main():
    if len(sys.argv) < 3:
        sys.exit('argv is error')
    while 1:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((sys.argv[1],int(sys.argv[2])))
        while 1:
            print('''============Welcome==============
  请选择：                        
      1.注册账号                  
      2.登录账号                  
      3.退出                     
=================================''')
            n = input('>>')
            if n == '1':
                zc(s)
            elif n == '2':
                dl(s)
            elif n == '3':
                sys.exit('退出')

if __name__ == '__main__':
    main()