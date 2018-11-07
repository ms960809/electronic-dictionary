# electronic-dictionary
电子词典的Python代码

dict_mysql.py为将字典文件dict.txt存入数据库的程序。
dict_client.py为电子词典客户端
dict_server.py为电子词典服务端


电子词典服务端
  1.使用多线程处理多个客户端的请求
  2.使用mysql数据库存储客户端用户信息
  3.使用tcp套接字进行通信
电子词典客户端
  1.使用tcp套接字进行通信
