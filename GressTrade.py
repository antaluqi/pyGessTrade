import Req,Comm
from config import *


class API():
    def __init__(self):
        pass

    def login(self,username,password):
        # 数据头
        GReqHead=Req.ReqHead()
        GReqHead.exch_code='8006'
        GReqHead.msg_type='1'
        GReqHead.msg_flag='1'
        GReqHead.term_type='03'
        GReqHead.user_type='2'
        GReqHead.user_id=username
        # 数据体
        v_reqMag=Req.ReqT8006()
        v_reqMag.bank_no=Constant['bank_no']
        v_reqMag.login_ip=Constant['login_ip']
        v_reqMag.net_agent='1'
        v_reqMag.net_envionment='2'
        v_reqMag.oper_flag='1'
        v_reqMag.user_id=username
        v_reqMag.user_id_type='1'
        v_reqMag.user_pwd=Comm.MD5(password)
        v_reqMag.user_type='2'
        # 数据头+数据体
        sMsg=GReqHead.ToString()+v_reqMag.ToString()
