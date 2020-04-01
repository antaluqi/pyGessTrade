from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime 
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit
import time
import sys
import api.GressTrade as gt

'''价格获取线程'''
class GetQuote_Thread(QThread):
    update_signal=pyqtSignal(str)

    def run(self):
        api=gt.API()
        islog,logMasg=api.login('1021805322','615919')
        print(logMasg)
        while True:
            api.getQuote2()
            s=api.quote.mautd.quoteTime+':  '+str(api.quote.mautd.last)
            self.update_signal.emit(s)

'''1s刷新线程'''
class Flash_1s_Thread(QThread):
    flash_signal=pyqtSignal()

    def run(self):
        while True:
            self.flash_signal.emit()
            time.sleep(1)

'''主函数'''
class Window(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.quoteStr='价格'
        self.initUI()
        self.initThread()

    '''界面初始化'''
    def initUI(self):
        self.setWindowTitle('PyQt 5界面实时更新例子')
        self.resize(400, 100)
        self.input = QLineEdit(self)
        self.input.resize(400, 100)

    '''线程初始化'''
    def initThread(self):
        # 创建线程
        self.getquote = GetQuote_Thread() 
        self.flash1s = Flash_1s_Thread()

        # 连接信号
        self.getquote.update_signal.connect(self.valueChange)
        self.flash1s.flash_signal.connect(self.flashInput)
        # 开始线程
        self.getquote.start()
        self.flash1s.start()

    def valueChange(self,data):
        self.quoteStr=data
    
    def flashInput(self):
        self.input.setText(self.quoteStr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show() 
    sys.exit(app.exec_())