# -*- coding: utf-8 -*-
import random
from datetime import datetime
from mysql_client_tools import MySQLConnector

# 初始化连接
connector = MySQLConnector(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='test'
)

# 插入单行数据
data = {'name': 'Alice', 'age': 20, 'created_at': datetime.now()}
connector.insert('users', data)

# 插入多行数据
data_list = [{'name': 'Bob', 'age': 25, 'created_at': datetime.now()},
             {'name': 'Charlie', 'age': 30, 'created_at': datetime.now()}]
connector.insert_many('users', data_list)

# 查询数据
result = connector.execute("SELECT * FROM users")
print(result)

# 查询单条数据
result = connector.execute("SELECT * FROM users WHERE name = %s", ('Alice',))
print(result)

# 查询多条数据
result = connector.execute("SELECT * FROM users WHERE age > %s", (25,))
print(result)

# 更新数据
data = {'age': random.randint(20, 40)}
where_clause = "name = %s"
connector.update('users', data, where_clause)

# 删除数据
where_clause = "age < %s"
connector.delete('users', where_clause)
