# -*- coding: utf-8 -*-
import sqlite3


class DB:
    
    def __init__(self,dbname):
        self._dbname = dbname
        self._conn = sqlite3.connect(dbname)
        self._cur = self._conn.cursor()

    """ DBからデータを全て取得する """
    def fetchall(self,tablename):
        self._cur.execute("select * from %s"%tablename)
        return self._cur.fetchall()

    """ DBを閉じる """
    def close(self):
        self._conn.close()

    def __isExist(self,tablename,key,value):
        target = self._cur.execute("SELECT * FROM %s where %s=%d"%(tablename,key,value)).fetchall()
        return True if len(target) != 0 else False


class ReportDB(DB):

    def __init__(self,dbname):
        super.__init__(dbname)

    """ DBに登録する """
    def insert(self,tablename,report):
        sql = "insert into %s (studentID,year,month,day,subject,socre,c1,c2,c3    ) values (?,?,?,?,?,?)"%tablename
        self._cur.execute(sql, report)
        self._conn.commit()

if __name__ == '__main__':
    pass
