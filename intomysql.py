import pymysql
import sys

def send():
    try: 
        db = pymysql.connect(host = 'localhost',user = 'root',password = '123456',
            database = 'dict',charset = 'utf8',port = 3306)
        cur = db.cursor()
    except:
        print('连接数据库失败')
        sys.exit(0)
    else: 
        print('正在插入....')
        with open('dict.txt') as f:
            for line in f:
                if not line:
                    break
                try:
                    cur.execute('insert into words(word,main) values'+ str((line[0:17].strip(),line[17:])))
                    db.commit()
                except:
                    db.rollback()
            db.close()
        f.close()
    print('插入成功')


if __name__ == '__main__':
    send()


