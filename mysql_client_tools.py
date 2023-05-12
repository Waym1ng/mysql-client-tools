# -*- coding: utf-8 -*-
import pymysql
from datetime import datetime
from pymysql import OperationalError
from dbutils.pooled_db import PooledDB

class MySQLClient:
    def __init__(self, host, port, user, password, database, charset='utf8mb4', max_connections=5):
        try:
            self.pool = PooledDB(
                creator=pymysql,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset=charset,
                autocommit=False,
                maxconnections=max_connections,
                cursorclass=pymysql.cursors.DictCursor
            )
        except OperationalError as e:
            print(f"Cannot connect to database: {e}")
            exit(1)

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """把字典里面的datetime对象转成字符串"""
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime)}
            result_dict.update(result_replace)
        return result_dict

    def execute(self, sql, params=None):
        """
        执行，返回的是 list，可单条也可多条
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        self.cursor = cursor

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            return [self.__dict_datetime_obj_to_str(row_dict) for row_dict in cursor.fetchall()]
        except Exception as e:
            print(f"Cannot execute query all: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def executemany(self, sql, params):
        """
        插入和更新时使用
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        self.cursor = cursor

        try:
            cursor.executemany(sql, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Cannot execute query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def query_one(self, sql, params=None):
        """
        返回的单条数据为dict
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        self.cursor = cursor

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            result = cursor.fetchone()
            return self.__dict_datetime_obj_to_str(result)
        except Exception as e:
            print(f"Cannot execute query one: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def insert(self, table, data):
        columns = ", ".join(data.keys())
        values_template = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values_template})"
        params = tuple(data.values())
        self.executemany(sql, [params])

    def insert_many(self, table, data_list):
        columns = ", ".join(data_list[0].keys())
        values_template = ", ".join(["%s"] * len(data_list[0]))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values_template})"
        params_list = [tuple(data.values()) for data in data_list]
        self.executemany(sql, params_list)

    def update(self, table, data, where_clause):
        set_clause = ", ".join([f"{key}=%s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(data.values())
        self.executemany(sql, [params])

    def delete(self, table, where_clause):
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        self.execute(sql)
