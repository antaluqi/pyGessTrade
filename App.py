from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime 
from PyQt5.QtWidgets import QApplication,  QDialog, QTextBrowser
import time
import sys
import sqlite3
import api.GressTrade as gt

'''sqllite3数据库接口'''
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

'''价格获取线程'''
class GetQuote_Thread(QThread):
    #update_signal=pyqtSignal()

    def __init__(self,api):
        QThread.__init__(self)
        self.api=api
       
    def run(self):
        api=self.api
        while True:
            try:
                api.getQuote2()
            except Exception as e:
                print(e)
            #self.update_signal.emit()

'''1s刷新线程'''
class Flash_window_Thread(QThread):
    flash_signal=pyqtSignal()
    def __init__(self,api):
        QThread.__init__(self)
        self.api=api
    def run(self):
        while True:
            try:
                self.api.getCustInfo()
            except Exception as e:
                print(e)
            self.flash_signal.emit()
            time.sleep(1)

'''数据库存储线程'''
class DB_Thread(QThread):
    # db_store_signal=pyqtSignal()
    def __init__(self,api,db):
        QThread.__init__(self)
        self.api=api
        self.db=db
    def run(self):
        ts0=''
        price0=0        
        while True:
            dt=self.api.quote.mautd.quoteDate
            dt=dt[0:4]+'-'+dt[4:6]+'-'+dt[6:]
            ts=self.api.quote.mautd.quoteTime
            price=self.api.quote.mautd.last
            if ts and ts!=ts0 and price!=price0:
              try:
                self.db.insertData('mautd',[dt,ts,price])
                ts0=ts
                price0=price
              except Exception as e:
                print(e)
              print('存储成功')
            else:
              print('数据为空或于上一数据相同')
            time.sleep(1)


'''主函数'''
class Window(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.stroeDB=False
        self.db=DB()
        self.api=gt.API()
        islog,logMasg=self.api.login('1021805322','615919')
        print(logMasg)
        if islog:
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
        # 价格获取线程
        self.getquote = GetQuote_Thread(self.api) 
        self.getquote.start()
        
        # 显示刷新线程
        self.flash1s = Flash_window_Thread(self.api)
        self.flash1s.flash_signal.connect(self.flashOutput)
        self.flash1s.start()

        # 数据库存储线程
        if self.stroeDB:
            self.dbstore = DB_Thread(self.api,self.db)
            self.dbstore.start()

    '''界面刷新'''
    def flashOutput(self):
       try:
         if self.api.custInfo.rsp_msg=='处理成功':
            s='时间：%s  标的: %s 价格: %s\r\n多单数: %s 均价: %s \r\n空单数：%s 均价: %s\r\n盈亏:%s'%(self.api.quote.mautd.quoteTime,self.api.custInfo.htm_td_info[0].td_prod_code,str(self.api.quote.mautd.last),
                                str(self.api.custInfo.htm_td_info[0].td_can_use_long),str(self.api.custInfo.htm_td_info[0].td_long_posi_avg_price),
                                str(self.api.custInfo.htm_td_info[0].td_can_use_short),str(self.api.custInfo.htm_td_info[0].td_short_posi_avg_price),
                                str(self.api.custInfo.r_surplus))
         else:
            s='-----'
        #self.Output.setText(self.api.quote.mautd.quoteTime+':  '+str(self.api.quote.mautd.last))

         self.Output.setText(s)
       except Exception as e:
           print(e)

    '''界面关闭时间触发'''
    def closeEvent(self,e):
       self.getquote.api.Close()
       self.db.close()
       print ("窗口关闭")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show() 
    sys.exit(app.exec_())