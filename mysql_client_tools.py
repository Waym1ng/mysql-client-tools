# -*- coding: utf-8 -*-
import pymysql
import datetime
from DBUtils.PooledDB import PooledDB
from config import mysql_config

class MySQLConnector:
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
                maxconnections=max_connections
            )
        except OperationalError as e:
            print(f"Cannot connect to database: {e}")
            exit(1)

    def execute(self, sql, params=None):
        conn = self.pool.connection()
        cursor = conn.cursor()

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            result = cursor.fetchall()
            if result:
                return self.convert_to_dict(result)
            else:
                return []
        except Exception as e:
            print(f"Cannot execute query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def executemany(self, sql, params):
        conn = self.pool.connection()
        cursor = conn.cursor()

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

    def convert_to_dict(self, result):
        converted_result = []
        for row in result:
            converted_row = {}
            for i, col in enumerate(cursor.description):
                value = row[i]
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                converted_row[col[0]] = value
            converted_result.append(converted_row)
        return converted_result

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
