# -*- coding: utf-8 -*-
import sqlite3

""" 
            ＜DB構造＞
    studentID  str   varchar(64)
    year       int           int
    month      int           int
    day        int           int
    subject    str   varchar(64)
    score      int           int
    c1         str   varchar(256)
    c2         str   varchar(256)
    c3         str   varchar(256)

    後、DBのインスタンス作ったらちゃんとclose()してね
"""

class DB:

    def __init__(self,dbname):
        self._dbname = dbname
        self._conn = sqlite3.connect(dbname)
        self._cur = self._conn.cursor()
        self._tablename = self.__getTableName()
    
    """ DBに登録する """
    def insert(self,reports):
        """ reportsはtupleのlist
        report = (studentID,year,month,day,subject,score,c1,c2,c3)
        reports = [report1,report2,report3,...,reportN]
        """
        sql = "insert into %s (studentID,year,month,day,subject,socre,c1,c2,c3) values (?,?,?,?,?,?)"%self._tablename
        for report in reports:
            self._cur.execute(sql, report)
        self._conn.commit()

    """ DBからデータを全て取得する """
    def fetchall(self):
        self._cur.execute("select * from %s"%self._tablename)
        return self._cur.fetchall()

    """ DBを閉じる """
    def close(self):
        self._conn.close()

    def __getTableName(self):
        self._cur.execute("select name from sqlite_master where type='table'")
        return self._cur.fetchall()[0][0]

    def __isExist(self,key,value):
        print(self._tablename)
        target = self._cur.execute("SELECT * FROM %s where %s=%d"%(self._tablename,key,value)).fetchall()
        return True if len(target) != 0 else False


if __name__ == '__main__':
    pass
