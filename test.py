from PyQt5.QtCore import QThread ,  pyqtSignal ,QMutex
from PyQt5.QtWidgets import QApplication,  QDialog, QTextBrowser
import time
import sys
import api.GressTrade as gt
import sqlite3
import random




class DB():
    def __init__(self):
        self.conn = sqlite3.connect("quote.db",check_same_thread = False)
        self.cursor = self.conn.cursor()

    # 创建表的sql语句
    def table_sql(self,table_name):
        sql={
            'mautd':'CREATE TABLE mautd (dt date,ts TIMESTAMP, price real)',
            'agtd':'CREATE TABLE agtd (dt date,ts TIMESTAMP, price real)'
        }
        if table_name not in sql:
            return False 
        return sql[table_name]

    # 表是否存在
    def has_table(self,table_name):
        if not self.table_sql(table_name):
            print('表%s 不存在且没有预设'%(table_name))
            return -2
        sql="select * from sqlite_master where type='table' and name = '%s'"%(table_name)
        self.cursor.execute(sql)
        if len(self.cursor.fetchall())==0:
            print('表%s 不存在但存在预设'%(table_name))
            return -1
        sql = "select * from sqlite_master where name='%s' and sql like '%%%s%%'"%(table_name,self.table_sql(table_name))
        self.cursor.execute(sql)
        if len(self.cursor.fetchall())==0:
            print('表%s 存在但于预设不符'%(table_name))
            return 0
        print('表%s 存在'%(table_name))
        return 1

    # 创建表
    def createTable(self,table_name):
        has_table=self.has_table(table_name)
        if has_table==-2:
            return False
        if has_table ==0:
           self.cursor.execute('drop table %s'%(table_name))
           print('删除表%s'%(table_name))
           self.cursor.execute(self.table_sql(table_name))
           print('创建表%s'%(table_name))
        elif has_table==-1:
           self.cursor.execute(self.table_sql(table_name))
           print('创建表%s'%(table_name))
        return True
    
    # 插入
    def insertData(self,table_name,values):
        vstr=''
        for v in values:
            vstr=vstr+"'"+str(v)+"',"
        sql = "insert into %s values(%s)"%(table_name,vstr[0:-1])
        self.cursor.execute(sql)
        self.conn.commit()

    # 查询
    def select(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 清空表
    def truncate(self,table_name):
        sql="delete from %s"%(table_name)
        self.cursor.execute(sql)
        self.conn.commit()

    # 关闭
    def close(self):
        self.cursor.close()
        self.conn.close()


qmut=QMutex()
'''价格获取线程'''
class GetQuote_Thread(QThread):
    update_signal=pyqtSignal()
    def __init__(self,db):
        QThread.__init__(self)
        self.db=db
    def run(self):
        while True:
            dt='2020-04-03'
            ts=time.strftime('%H:%M:%S',time.localtime(time.time()))
            price=random.random()*1000
            try:
                qmut.lock()
                self.db.insertData('mautd',[dt,ts,price])
                qmut.unlock()
            except Exception as e:
                print(e)
            print('insert success!')
            self.update_signal.emit()
            time.sleep(1)

'''1s刷新线程'''
class Flash_1s_Thread(QThread):
    flash_signal=pyqtSignal()
    def __init__(self,db):
        QThread.__init__(self)
        self.db=db
    def run(self):
        time.sleep(0.1)
        while True:
            try:
              qmut.lock()
              r=self.db.select('select * from mautd')
              qmut.unlock()
              print(r)
            except Exception as e:
                print(e)
            time.sleep(1)

'''主函数'''
class Window(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.db=DB()
        
        self.initUI()
        self.initThread()
            

    '''界面初始化'''
    def initUI(self):
        self.setWindowTitle('PyQt 5界面实时更新例子')
        self.resize(500, 200)
        self.Output = QTextBrowser(self)
        self.Output.resize(500, 200)

    '''线程初始化'''
    def initThread(self):
        # 创建线程
        self.getquote = GetQuote_Thread(self.db) 
        self.flash1s = Flash_1s_Thread(self.db)

        # 连接信号
        #self.flash1s.flash_signal.connect(self.flashOutput)
        # 开始线程
        self.getquote.start()
        self.flash1s.start()

    
    def flashOutput(self):
        pass
    def closeEvent(self,e):
       self.db.close()
       print ("窗口关闭")

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = Window()
        win.show() 
        sys.exit(app.exec_())
    