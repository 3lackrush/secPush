#!/usr/bin/env python
#--*-- coding:utf-8 --*--

import pymysql
from termcolor import colored

class secPushSQL(object):

    def __init__(self,MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASS,MYSQL_DBNAME):
        self.host = MYSQL_HOST
        self.port = MYSQL_PORT
        self.user = MYSQL_USER
        self.pwd = MYSQL_PASS
        self.dbname = MYSQL_DBNAME
        self.db = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DBNAME,charset='utf8')
        self.cursor = self.db.cursor()

    def _createTable(self):
        SQL = "CREATE TABLE IF NOT EXISTS secpushinfo (id int PRIMARY KEY AUTO_INCREMENT, title varchar(128), link varchar(128), dateinfo varchar(128))"
        self.cursor.execute(SQL)

    def insert2db(self, query):
        try:
            SQL = "INSERT INTO secpushinfo (title, link, dateinfo ) VALUES (%s, %s, %s)"
            print(colored(SQL, "green"), colored(query, "red"))
            self.cursor.execute(SQL,query)
            self.db.commit()
        except Exception as e:
            self.db.rollback()

    def getFeedFromDb(self):
        reslist = []
        try:
            SQL = "SELECT * from secpushinfo"
            self.cursor.execute(SQL)
            res = self.cursor.fetchall()
            for each in res:
                tmp_dic = {}
                tmp_dic["title"] = each[1]
                tmp_dic["url"] = each[2]
                reslist.append(tmp_dic)
            return reslist
        except Exception as e:
            print(str(e))

    def delFeed(self):
        try:
            SQL = "DELETE FROM secpushinfo"
            self.cursor.execute(SQL)
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    obj1 = secPushSQL('127.0.0.1',3306,'root','redhat','secpush')
    obj1.getFeedFromDb()
