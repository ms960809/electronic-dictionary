#!usr/bin/env python3 
#coding:utf-8

import pymysql
import re
import sys
 

def insql():
    try:
        db = pymysql.connect('0.0.0.0','root','123456','dict',3306)
    except:
        sys.exit('连接数据库失败!')
    cur = db.cursor()
    with open('dict.txt') as f:
        i = 1
        for line in f:
            word = re.search(r'\S+\b',line).group()
            if len(word) <= 17:
                word = line[:17].strip()
                fanyi = line[17:].strip()
            else:
                fanyi = line[len(word):]
            try:
                cur.execute('insert into dict values'+str((word,fanyi)))
            except:
                db.rollback()
                db.close()
                print('')
                sys.exit('写入失败!')
            i += 1
            print(i + 1,end = '\r')
        print('\n')
        print('写入完成！')
        db.commit()
        db.close


if __name__ == '__main__':
    insql()

def history(s):
    name = input("输入要查询历史的用户：")
    msg = "H {}".format(name)
    print(name)
    s.send(msg.encode())
    data = s.recv(2048).decode()
    data = data.split("#")


    n = 0
    x = PrettyTable(["<<$ID$>>","<<$name$>>","<<$word$>>","<<$date$>>"])
    while True:
        x.add_row([data[1+n],data[2+n],data[3+n],data[4+n]])
        n += 4
        if n >= len(data)-4:
            break

    print(x)