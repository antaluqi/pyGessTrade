from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime 
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit,QTextBrowser
import time
import sys
import api.GressTrade as gt

'''价格获取线程'''
class GetQuote_Thread(QThread):
    update_signal=pyqtSignal()

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
            self.update_signal.emit()

'''1s刷新线程'''
class Flash_1s_Thread(QThread):
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

'''主函数'''
class Window(QDialog):

    def __init__(self):
        QDialog.__init__(self)
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
        # 创建线程
        self.getquote = GetQuote_Thread(self.api) 
        self.flash1s = Flash_1s_Thread(self.api)

        # 连接信号
        self.flash1s.flash_signal.connect(self.flashOutput)
        # 开始线程
        self.getquote.start()
        self.flash1s.start()

    
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
    def closeEvent(self,e):
       self.getquote.api.Close()
       print ("窗口关闭")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show() 
    sys.exit(app.exec_())