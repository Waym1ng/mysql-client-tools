# -*- coding: utf-8 -*-
import json
import pymysql
import datetime
from DBUtils.PooledDB import PooledDB
from config import mysql_config



class MysqlClient(object):
    __pool = None

    def __init__(self, mysql_config):
        """
        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param host:数据库ip地址
        :param port:数据库端口
        :param database:库名
        :param user:用户名
        :param password:密码
        :param charset:字符编码
        """
        mincached = 10
        maxcached = 20
        maxshared = 10
        maxconnections = 100
        blocking = True
        host = mysql_config.get("HOST")
        port = mysql_config.get("PORT")
        database = mysql_config.get("DATABASE")
        user = mysql_config.get("USERNAME")
        password = mysql_config.get("PASSWORD")
        charset = 'utf8mb4'

        if not self.__pool:
            self.__class__.__pool = PooledDB(pymysql,
                                             mincached, maxcached, maxshared, maxconnections, blocking,
                                             host=host, port=port, database=database,
                                             user=user, password=password,
                                             charset=charset,
                                             cursorclass=pymysql.cursors.DictCursor
                                             )
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __del__(self):
        if self._conn and self._cursor:
            self.__close()

    def __get_conn(self):
        self._conn = self.__pool.connection()
        self._cursor = self._conn.cursor()

    def __close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            raise e

    def __execute(self, sql, param=()):
        count = self._cursor.execute(sql, param)
        return count

    def __commit(self):
        '''提交'''
        try:
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise e

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """把字典里面的datetime对象转成字符串，使json转换不出错"""
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
            result_dict.update(result_replace)
        return result_dict

    def select_one(self, sql, param=()):
        """查询单个结果"""
        self.__execute(sql, param)
        result = self._cursor.fetchone()
        if not result:
            return dict()
        """:type result:dict"""
        result = self.__dict_datetime_obj_to_str(result)
        return result

    def select_many(self, sql, param=()):
        """
        查询多个结果
        :param sql: qsl语句
        :param param: sql参数
        :return: 结果数量和查询结果集
        """
        self.__execute(sql, param)
        result = self._cursor.fetchall()
        """:type result:list"""
        [self.__dict_datetime_obj_to_str(row_dict) for row_dict in result]
        return result

    def execute_count(self, sql, param=()):
        '''返回结果的数量'''
        count = self.__execute(sql, param)
        return count

    def insert(self, sql, param=()):
        """插入行"""
        result = self.__execute(sql, param)
        self.__commit()
        return result

    def insert_dict(self, table, data):
        """通过 dict 插入数据"""
        # 获取到一个以键且为逗号分隔的字符串，返回一个字符串
        keys = ','.join(data.keys())
        param = list(data.values())
        s_len = ','.join(['%s'] * len(data))
        sql = f'''insert into {table}(%s) values(%s)'''
        insert_sql = sql % (keys, s_len)
        result = self.__execute(insert_sql, param)
        self.__commit()
        return result

    def update(self, sql, param=()):
        '''更新'''
        result = self.__execute(sql, param)
        self.__commit()
        return result

    def batch_update(self, sql, param=()):
        '''批量更新'''
        result = self._cursor.executemany(sql, param)
        self.__commit()
        return result

    def delete(self, sql, param=()):
        '''删除'''
        result = self.__execute(sql, param)
        self.__commit()
        return result
