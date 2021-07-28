# -*- coding: utf-8 -*-
from mysql_client_tools import MysqlClient


if __name__ == "__main__":
    mc = MysqlClient()

    sql = 'SELECT * FROM users WHERE id=2'
    result = mc.select_one(sql)
    print(result)
    '''{'id': 2, 'email': '888@qq.com', 'status': 1}'''

    sql = 'SELECT * FROM users'
    result = mc.select_many(sql)
    print('更新前：', result)
    '''更新前： (4, [{'id': 2, 'email': '888@qq.com', 'status': 1}, {'id': 3, 'email': '777@qq.com', 'status': 1}, {'id': 4, 'email': '666@qq.com', 'status': 1}, {'id': 5, 'email': '555@qq.com', 'status': 1}])'''

    # 批量更新时传入列表
    batch_update_sql = 'UPDATE users SET status=0 WHERE id=(%s)'
    result = mc.batch_update(batch_update_sql, ([2, 3, 4]))
    print('更新成功的条数：', result)
    '''更新成功的条数： 3'''

    sql = 'SELECT * FROM users'
    result = mc.select_many(sql)
    print('更新后：', result)
    '''更新后： (4, [{'id': 2, 'email': '888@qq.com', 'status': 0}, {'id': 3, 'email': '777@qq.com', 'status': 0}, {'id': 4, 'email': '666@qq.com', 'status': 0}, {'id': 5, 'email': '555@qq.com', 'status': 1}])'''
    # sql = 'INSERT INTO users (email, status) VALUES (%s, %s)'
    # result = mc.insert(sql, ("444@qq.com", 1))
    # print('添加成功的条数：', result)
    # '''添加成功的条数： 1'''

    # 测试日期
    sql = 'SELECT * FROM items'
    result = mc.select_many(sql)
    print('测试日期：', result)
    '''测试日期： (1, [{'id': 1, 'title': '12345', 'create_time': '2021-07-28 14:39:08'}])'''