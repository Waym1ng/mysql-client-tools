# mysql-client-tools
## 说明
- 使用`pymysql`连接MySQL数据库，`PooledDB`连接池的用法，以及对CURD的封装
- 查询时，对MySQL中datetime格式的字段，自动转换成时间格式字符串
- 封装了`select_one` `select_many` `insert` `update` `batch_update` `delete`的方法
- 对执行原生sql有效，不使用拼接字符串的sql语句，params作为参数传入查询中

## 使用
- 在`config.py` 中配置好MySQL的信息(host，password等)
- `mc = MysqlClient()` 实例化后即可使用

## 结果
- 可以查看`demo.py`文件
