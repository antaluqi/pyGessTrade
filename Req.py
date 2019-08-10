import Comm
from config import *
import datetime
class ReqHead():
    def __init__(self):
        self.area_code = ""
        self.branch_id = ""
        self.c_teller_id1 = ""
        self.c_teller_id2 = ""
        self.exch_code = ""
        self.msg_flag = ""
        self.msg_len = ""
        self.msg_type = ""
        self.seq_no = ""
        self.term_type = ""
        self.user_id = ""
        self.user_type = ""

    def GetSeqNo(self):
        num=Constant['SEQ_NO']+1
        if num==10:
            num=0
        Constant['SEQ_NO']=num
        return hex(int(datetime.datetime.now().strftime('%H%M%S%f')[0:-3]))[2:]+str(num)

    def ToString(self):
        self.seq_no=self.GetSeqNo()
        str=Comm.Fill(self.seq_no,' ',8,'R')+\
            Comm.Fill(self.msg_type,' ',1,'R')+ \
            Comm.Fill(self.exch_code,' ',4,'R')+ \
            Comm.Fill(self.msg_flag,' ',1,'R')+ \
            Comm.Fill(self.term_type,' ',2,'R')+ \
            Comm.Fill(self.user_type,' ',2,'R')+ \
            Comm.Fill(self.user_id,' ',10,'R')+ \
            Comm.Fill(self.area_code,' ',4,'R')+ \
            Comm.Fill(self.branch_id,' ',12,'R')+ \
            Comm.Fill(self.c_teller_id1,' ',10,'R')+ \
            Comm.Fill(self.c_teller_id2,' ',10,'R')
        return str



'''
消息基础类
'''
class ReqBase(object):

    def ToString(self):
        fields=vars(self)
        str='#'
        for k,v in fields.items():
            str=str+k+'='+v+'#'
        return str


'''
登陆的消息类
'''
class ReqT8006(ReqBase):
    def __init__(self):
        self.bank_no = ''
        self.login_ip = ''
        self.net_agent = ''
        self.net_envionment = ''
        self.oper_flag = '0'
        self.user_id = ""
        self.user_id_type = ''
        self.user_pwd = ""
        self.user_type = ''
