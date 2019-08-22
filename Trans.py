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
发送消息基础类
'''
class ReqBase(object):

    def ToString(self):
        fields=vars(self)
        strR='#'
        for k,v in fields.items():
            if v!='':
               strR=strR+k+'='+str(v)+'#'
        return strR


'''
登陆的发送消息类
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


'''
关闭发送的消息类
'''

class ReqT8002(ReqBase):
    def __init__(self):
        self.oper_flag='0'
        self.user_id=""
        self.user_type=""

'''
交易的发送消息类
'''
class ReqP4001(ReqBase):
    def __init__(self):
        self.acct_no = ""
        self.b_market_id = ""
        self.bank_no = ""
        self.bs = ""
        self.client_serial_no = ""
        self.cov_type = ""
        self.cust_id = ""
        self.deli_flag = ""
        self.entr_amount = 0
        self.entr_price = ""
        self. match_type = "1"
        self.offset_flag = ""
        self.oper_flag = 1
        self.order_send_type = "1"
        self. prod_code = ""
        self.src_match_no = ""


class ReqT4041(ReqP4001):
    def __init__(self):
        super(ReqT4041, self).__init__()
        self.b_market_id = "02"
        self.bs = "b"
        self.deli_flag = ""
        self.offset_flag = "0"

'''
获取客户信息的发送类
'''
class ReqT1020(ReqBase):

    def __init__(self):
        self.acct_no = ""
        self.is_check_stat = "1"
        self.oper_flag = 0
        self.qry_cust_info = "0"
        self.qry_defer = "0"
        self.qry_forward = "0"
        self.qry_fund = "0"
        self.qry_storage = "0"
        self.qry_surplus = "0"


'''
交易信息查询的发送类
'''
class ReqT6002(ReqBase):
    def __init__(self):
        # public ArrayListMsg alm_view_field = new ArrayListMsg();
        self.alm_view_field=""
        self.curr_page = 1
        self.login_branch_id = ""
        self.login_teller_id = ""
        self.oper_flag = 1
        self.paginal_num = 0
        self.query_id = ""

        self.prod_code=""
        self.exch_code=""
        self.b_offset_flag=""

    def ToString(self):
        fields=vars(self)
        strR='#'
        for k,v in fields.items():
                strR=strR+k+'='+str(v)+'#'
        return strR

'''
获取报价的发送消息类
'''
class GBcMsgReqLink(ReqBase):
    def __init__(self):
        self.RspCode = ''
        self.RspMsg = ''
        self.again_flag = ''
        self.branch_id = ''
        self.cust_type_id = ''
        self.is_lfv = ''
        self.lan_ip = ''
        self.term_type = ''
        self.user_id = ''
        self.user_key = ''
        self.user_pwd = ''
        self.user_type = ''
        self.www_ip = ''

    def  ToString(self):
        fields=vars(self)
        str='#'
        for k,v in fields.items():
            if v!='':
                str=str+k+'='+v+'#'
        return str

# =====================================================================================================================
# Rsp
# =====================================================================================================================
'''
返回消息基础类
'''
class RspBase(object):

    def ToString(self):
        reStr=''
        for k,v in vars(self).items():
            reStr=reStr+str(k)+'='+str(v)+'\n'
        return reStr

'''
服务器返回登陆信息的储存类
'''
class ServerInfo(RspBase):
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

    def ToString(self):
        reStr=''
        for k,v in vars(self).items():
            reStr=reStr+str(k)+'='+str(v)+'\n'
        return reStr
'''
返回客户信息的储存类
'''
class CustomerInfo(RspBase):

    def __init__(self):
        self.rsp_msg=''
        self.oper_flag=0
        self.c_acct_no=''
        self.c_cust_id=''
        self.c_account_no=''
        self.c_open_bank_name=''
        self.c_cust_abbr=''
        self.c_b_fare_model_id=''
        self.c_m_fare_model_id=''
        self.c_acct_type=0
        self.c_ocma_flag=0
        self.c_acct_stat=0
        self.c_cert_type=''
        self.c_cert_num=''
        self.c_branch_id=''
        self.f_currency_id=1
        self.f_curr_bal=.43
        self.f_can_use_bal=.43
        self.f_can_get_bal=0.43
        self.f_in_bal=0
        self.f_out_bal=0
        self.f_buy_bal=0
        self.f_sell_bal=0
        self.f_exch_froz_bal=0
        self.f_posi_margin=0
        self.f_base_margin=0
        self.f_take_margin=0
        self.f_stor_margin=0
        self.f_pt_reserve=0
        self.f_ag_margin=0
        self.f_forward_froz=0
        self.f_exch_fare=0
        self.r_surplus=0.00
        self.f_offset_quota=0
        self.f_avaliable_offset_quota=0
        self.f_used_offset_quota=0
        self.f_offset_entr_margin=0

    def fromString(self,CustStr):
        msgTuple = re.findall(r'(.*?)=(.*?)#', CustStr.split('#', 1)[1], re.M | re.I)
        CustInfoMap={}
        CustInfoMap.update(msgTuple)
        if CustInfoMap['rsp_msg'] == '处理成功':
            self.rsp_msg = CustInfoMap['rsp_msg']
            self.oper_flag = int(CustInfoMap['oper_flag'])
            self.c_acct_no = CustInfoMap['c_acct_no']
            self.c_cust_id = CustInfoMap['c_cust_id']
            self.c_account_no = CustInfoMap['c_account_no']
            self.c_open_bank_name = CustInfoMap['c_open_bank_name']
            self.c_cust_abbr = CustInfoMap['c_cust_abbr']
            self.c_b_fare_model_id = CustInfoMap['c_b_fare_model_id']
            self.c_m_fare_model_id = CustInfoMap['c_m_fare_model_id']
            self.c_acct_type = int(CustInfoMap['c_acct_type'] )
            self.c_ocma_flag = int(CustInfoMap['c_ocma_flag'] )
            self.c_acct_stat = int(CustInfoMap['c_acct_stat'] )
            self.c_cert_type = CustInfoMap['c_cert_type']
            self.c_cert_num = CustInfoMap['c_cert_num']
            self.c_branch_id = CustInfoMap['c_branch_id']
            self.f_currency_id = int(CustInfoMap['f_currency_id'] )
            self.f_curr_bal = float(CustInfoMap['f_curr_bal'] )
            self.f_can_use_bal = float(CustInfoMap['f_can_use_bal'] )
            self.f_can_get_bal = float(CustInfoMap['f_can_get_bal'] )
            self.f_in_bal = float(CustInfoMap['f_in_bal'] )
            self.f_out_bal = float(CustInfoMap['f_out_bal'] )
            self.f_buy_bal = float(CustInfoMap['f_buy_bal'] )
            self.f_sell_bal = float(CustInfoMap['f_sell_bal'] )
            self.f_exch_froz_bal = float(CustInfoMap['f_exch_froz_bal'] )
            self.f_posi_margin = float(CustInfoMap['f_posi_margin'] )
            self.f_base_margin = float(CustInfoMap['f_base_margin'] )
            self.f_take_margin = float(CustInfoMap['f_take_margin'] )
            self.f_stor_margin = float(CustInfoMap['f_stor_margin'] )
            self.f_pt_reserve = float(CustInfoMap['f_pt_reserve'] )
            self.f_ag_margin = float(CustInfoMap['f_ag_margin'] )
            self.f_forward_froz = float(CustInfoMap['f_forward_froz'] )
            self.f_exch_fare = float(CustInfoMap['f_exch_fare'] )
            self.r_surplus = float(CustInfoMap['r_surplus'] )
            self.f_offset_quota = float(CustInfoMap['f_offset_quota'] )
            self.f_avaliable_offset_quota = float(CustInfoMap['f_avaliable_offset_quota'] )
            self.f_used_offset_quota = float(CustInfoMap['f_used_offset_quota'] )
            self.f_offset_entr_margin = float(CustInfoMap['f_offset_entr_margin'] )

class QuoteItem(RspBase):
    def __init__(self):
        self.ApiName=''
        self.RspMsg=''
        self.instID=''
        self.quoteDate=''
        self.RspCode=''
        self.upDownRate = 0
        self.quoteTime = ''
        self.sequenceNo = 0
        self.average = 0
        self.turnOver = 0
        self.upDown = 0
        self.Posi = 0
        self.lowLimit = 0
        self.highLimit = 0
        self.weight = 0
        self.volume = 0
        self.askLot5 = 0
        self.ask5 = 0
        self.askLot4 = 0
        self.ask4 = 0
        self.askLot3 = 0
        self.ask3 = 0
        self.askLot2 = 0
        self.ask2 = 0
        self.askLot1 = 0
        self.ask1 = 0
        self.bidLot5 = 0
        self.bid5 = 0
        self.bidLot4 = 0
        self.bid4 = 0
        self.bidLot3 = 0
        self.bid3 = 0
        self.bidLot2 = 0
        self.bid2 = 0
        self.bidLot1 = 0
        self.bid1 = 0
        self.settle = 0
        self.close = 0
        self.last = 0
        self.low = 0
        self.high = 0
        self.open = 0
        self.lastClose = 0
        self.lastSettle = 0
    def fromDict(self,qDict):
        for k in qDict.keys():
            v=qDict[k]
            if k=='sZipBuff':
                for kk in v.keys():
                    vv=qDict[k][kk]
                    if kk=='quoteTime':
                        exec('self.'+kk+'=vv')
                    else:
                        exec('self.'+kk+'=float(vv)')
            else:
                exec('self.'+k+'=v')
        return

class Quote(object):
    def __init__(self):
        self.au9999 = QuoteItem()
        self.au100g = QuoteItem()
        self.iau9999 = QuoteItem()
        self.au50g = QuoteItem()
        self.iau100g = QuoteItem()
        self.au9995 = QuoteItem()
        self.autn2 = QuoteItem()
        self.agtd = QuoteItem()
        self.autn1 = QuoteItem()
        self.autd = QuoteItem()
        self.ag9999 = QuoteItem()
        self.au995 = QuoteItem()
        self.ag999 = QuoteItem()
        self.pgc30g = QuoteItem()
        self.iau995 = QuoteItem()
        self.pt9995 = QuoteItem()
        self.mautd = QuoteItem()
    def fromDict(self,qDict):
        if 'instID' in qDict:
            key=qDict['instID']
            exec('self.'+re.sub('[.+()]','',key).lower()+'.fromDict(qDict)')
        return


