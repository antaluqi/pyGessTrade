import Comm
from config import *
import datetime
import re
# =====================================================================================================================
# Req
# =====================================================================================================================
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



# =====================================================================================================================
# Rsp
# =====================================================================================================================

class ServerInfo():
    def __init__(self):
        self.user_id=''
        self.branch_id=''
        self.city_code=''
        self.broadcast_ip=''
        self.broadcast_port=0
        self.fund_trans_ip=''
        self.fund_trans_port=0
        self.query_ip=''
        self.query_port=0
        self.risk_broadcast_ip=''
        self.risk_broadcast_port=0
        self.risk_trans_ip=''
        self.risk_trans_port=0
        self.server_code=''
        self.server_name=''
        self.trans_ip=''
        self.trans_port=0
        self.oper_flag=None
        self.rsp_msg=''
        self.session_id=''
        self.session_key=''

    def fromString(self,logSevStr):
        msgTuple=re.findall( r'(.*?)=(.*?)#',logSevStr.split('#',1)[1], re.M|re.I)
        logInfoMap={}
        logInfoMap.update(msgTuple)
        self.rsp_msg=logInfoMap['rsp_msg']
        if logInfoMap['rsp_msg']=='处理成功':
            hsl=logInfoMap['htm_server_list'].split('∧')
            hsl_key_list=hsl[0].split('｜')
            hsl_value_list=hsl[1].split('ˇ')
            hslInfo={}
            hslInfo.update(zip(hsl_key_list[0:-1],hsl_value_list[0:-1]))
            logInfoMap['htm_server_list']=hslInfo

            self.branch_id=logInfoMap['branch_id']
            self.city_code=logInfoMap['city_code']

            self.broadcast_ip=logInfoMap['htm_server_list']['broadcast_ip']
            self.broadcast_port=logInfoMap['htm_server_list']['broadcast_port']
            self.broadcast_port=0 if self.broadcast_port=='' else int(self.broadcast_port)

            self.fund_trans_ip=logInfoMap['htm_server_list']['fund_trans_ip']
            self.fund_trans_port=logInfoMap['htm_server_list']['fund_trans_port']
            self.fund_trans_port=0 if self.fund_trans_port=='' else int(self.fund_trans_port)

            self.query_ip=logInfoMap['htm_server_list']['query_ip']
            self.query_port=logInfoMap['htm_server_list']['query_port']
            self.query_port=0 if self.query_port=='' else int(self.query_port)

            self.risk_broadcast_ip=logInfoMap['htm_server_list']['risk_broadcast_ip']
            self.risk_broadcast_port=logInfoMap['htm_server_list']['risk_broadcast_port']
            self.risk_broadcast_port=0 if self.risk_broadcast_port=='' else int(self.risk_broadcast_port)

            self.risk_trans_ip=logInfoMap['htm_server_list']['risk_trans_ip']
            self.risk_trans_port=logInfoMap['htm_server_list']['risk_trans_port']
            self.risk_trans_port=0 if self.risk_trans_port=='' else int(self.risk_trans_port)

            self.server_code=logInfoMap['htm_server_list']['server_code']
            self.server_name=logInfoMap['htm_server_list']['server_name']

            self.trans_ip=logInfoMap['htm_server_list']['trans_ip']
            self.trans_port=logInfoMap['htm_server_list']['trans_port']
            self.trans_port=0 if self.trans_port=='' else int(self.trans_port)

            self.oper_flag=logInfoMap['oper_flag']
            self.rsp_msg=logInfoMap['rsp_msg']
            self.session_id=logInfoMap['session_id']
            self.session_key=logInfoMap['session_key']


