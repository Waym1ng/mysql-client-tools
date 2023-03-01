# mysql-client-tools
以下是使用Python连接MySQL数据库的代码和使用方法，代码支持查询、插入、更新和删除操作，使用了连接池提高了性能和可靠性。

准备工作
在使用代码之前，需要先安装好pymysql和DBUtils模块。可以使用以下命令进行安装：

bash
Copy code
pip install pymysql
pip install dbutils
使用方法
连接数据库
首先需要创建一个MySQLConnector对象，用于连接数据库。构造函数需要传入MySQL服务器的连接信息，包括主机名、端口号、用户名、密码、数据库名等参数。其中max_connections参数表示连接池中最大连接数，默认为5。

python
Copy code
from mysql_connector import MySQLConnector

conn = MySQLConnector(host='localhost', port=3306, user='root', password='password', database='mydb', max_connections=10)
查询数据
查询数据可以使用execute方法，该方法接收一个SQL语句和可选的参数列表作为参数，返回一个包含查询结果的字典列表。如果查询结果为空，则返回一个空列表。查询中如果有datetime类型的字段，会自动转换为字符串类型输出。

python
Copy code
result = conn.execute("SELECT * FROM mytable")
print(result)
插入数据
插入单行数据可以使用insert方法，该方法接收两个参数，分别为表名和一个包含数据的字典，其中字典的键为字段名，值为要插入的数据。插入多行数据可以使用insert_many方法，该方法接收两个参数，分别为表名和一个包含多个数据字典的列表，列表中的每个字典表示一行要插入的数据。

python
Copy code
data = {'name': 'Alice', 'age': 20, 'created_at': datetime.now()}
conn.insert('mytable', data)

data_list = [
    {'name': 'Bob', 'age': 25, 'created_at': datetime.now()},
    {'name': 'Charlie', 'age': 30, 'created_at': datetime.now()}
]
conn.insert_many('mytable', data_list)
更新数据
更新数据可以使用update方法，该方法接收三个参数，分别为表名、一个包含要更新的数据的字典和一个表示更新条件的字符串，更新条件的格式为SQL中WHERE子句的格式。

python
Copy code
data = {'age': 21}
conn.update('mytable', data, 'name="Alice"')
删除数据
删除数据可以使用delete方法，该方法接收两个参数，分别为表名和一个表示删除条件的字符串，删除条件的格式为SQL中WHERE子句的格式。

python
Copy code
conn.delete('mytable', 'age=25')
