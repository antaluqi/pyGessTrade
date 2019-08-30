import Comm
from config import *
import datetime
import re

# =====================================================================================================================
# Req
# =====================================================================================================================
'''消息头'''


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

    def getSeqNo(self):
        num = Constant['SEQ_NO'] + 1
        if num == 10:
            num = 0
        Constant['SEQ_NO'] = num
        return hex(int(datetime.datetime.now().strftime('%H%M%S%f')[0:-3]))[2:] + str(num)

    def toString(self):
        self.seq_no = self.getSeqNo()
        str = Comm.Fill(self.seq_no, ' ', 8, 'R') + \
              Comm.Fill(self.msg_type, ' ', 1, 'R') + \
              Comm.Fill(self.exch_code, ' ', 4, 'R') + \
              Comm.Fill(self.msg_flag, ' ', 1, 'R') + \
              Comm.Fill(self.term_type, ' ', 2, 'R') + \
              Comm.Fill(self.user_type, ' ', 2, 'R') + \
              Comm.Fill(self.user_id, ' ', 10, 'R') + \
              Comm.Fill(self.area_code, ' ', 4, 'R') + \
              Comm.Fill(self.branch_id, ' ', 12, 'R') + \
              Comm.Fill(self.c_teller_id1, ' ', 10, 'R') + \
              Comm.Fill(self.c_teller_id2, ' ', 10, 'R')
        return str


'''发送消息基础类'''


class ReqBase(object):

    def toString(self):
        fields = vars(self)
        strR = '#'
        for k, v in fields.items():
            if v != '':
                strR = strR + k + '=' + str(v) + '#'
        return strR


'''登陆的发送消息类'''


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


'''关闭发送的消息类'''


class ReqT8002(ReqBase):
    def __init__(self):
        self.oper_flag = '0'
        self.user_id = ""
        self.user_type = ""


'''交易的发送消息类'''


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
        self.match_type = "1"
        self.offset_flag = ""
        self.oper_flag = 1
        self.order_send_type = "1"
        self.prod_code = ""
        self.src_match_no = ""


'''开多'''


class ReqT4041(ReqP4001):
    def __init__(self):
        super(ReqT4041, self).__init__()
        self.b_market_id = "02"
        self.bs = "b"
        self.deli_flag = ""
        self.offset_flag = "0"


'''开空'''


class ReqT4042(ReqP4001):
    def __init__(self):
        super(ReqT4042, self).__init__()
        self.b_market_id = "02"
        self.bs = "s"
        self.deli_flag = ""
        self.offset_flag = "0"


'''平多'''


class ReqT4043(ReqP4001):
    def __init__(self):
        super(ReqT4043, self).__init__()
        self.b_market_id = "02"
        self.bs = "s"
        self.cov_type = '1'
        self.deli_flag = ""
        self.offset_flag = "1"


'''平空'''


class ReqT4044(ReqP4001):
    def __init__(self):
        super(ReqT4044, self).__init__()
        self.b_market_id = "02"
        self.bs = "b"
        self.cov_type = '1'
        self.deli_flag = ""
        self.offset_flag = "1"


'''撤单发送类'''


class ReqT4061(ReqBase):
    def __init__(self):
        self.cancel_order_no = ''
        self.oper_flag = 0


'''获取客户信息的发送类'''


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


'''交易信息查询的发送类'''


class ReqT6002(ReqBase):
    def __init__(self):
        # public ArrayListMsg alm_view_field = new ArrayListMsg();
        self.alm_view_field = ""
        self.curr_page = 1
        self.login_branch_id = ""
        self.login_teller_id = ""
        self.oper_flag = 1
        self.paginal_num = 0
        self.query_id = ""

        self.prod_code = ""
        self.exch_code = ""
        self.b_offset_flag = ""

    def toString(self):
        fields = vars(self)
        strR = '#'
        for k, v in fields.items():
            strR = strR + k + '=' + str(v) + '#'
        return strR


'''获取报价的发送消息类'''


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

    def toString(self):
        fields = vars(self)
        str = '#'
        for k, v in fields.items():
            if v != '':
                str = str + k + '=' + v + '#'
        return str


# =====================================================================================================================
# Rsp
# =====================================================================================================================

'''返回消息基础类'''


class RspBase(object):

    def toString(self):
        reStr = ''
        for k, v in vars(self).items():
            reStr = reStr + str(k) + '=' + str(v) + '\n'
        return reStr

    def toDict(self):
        return vars(self).copy()


'''
服务器返回登陆信息的储存类
'''


class ServerInfo(RspBase):
    def __init__(self):
        self.user_id = ''
        self.branch_id = ''
        self.city_code = ''
        self.broadcast_ip = ''
        self.broadcast_port = 0
        self.fund_trans_ip = ''
        self.fund_trans_port = 0
        self.query_ip = ''
        self.query_port = 0
        self.risk_broadcast_ip = ''
        self.risk_broadcast_port = 0
        self.risk_trans_ip = ''
        self.risk_trans_port = 0
        self.server_code = ''
        self.server_name = ''
        self.trans_ip = ''
        self.trans_port = 0
        self.oper_flag = None
        self.rsp_msg = ''
        self.session_id = ''
        self.session_key = ''

    def fromString(self, logSevStr):
        msgTuple = re.findall(r'(.*?)=(.*?)#', logSevStr.split('#', 1)[1], re.M | re.I)
        logInfoMap = {}
        logInfoMap.update(msgTuple)
        self.rsp_msg = logInfoMap['rsp_msg']
        if logInfoMap['rsp_msg'] == '处理成功':
            hsl = logInfoMap['htm_server_list'].split('∧')
            hsl_key_list = hsl[0].split('｜')
            hsl_value_list = hsl[1].split('ˇ')
            hslInfo = {}
            hslInfo.update(zip(hsl_key_list[0:-1], hsl_value_list[0:-1]))
            logInfoMap['htm_server_list'] = hslInfo

            self.branch_id = logInfoMap['branch_id']
            self.city_code = logInfoMap['city_code']

            self.broadcast_ip = logInfoMap['htm_server_list']['broadcast_ip']
            self.broadcast_port = logInfoMap['htm_server_list']['broadcast_port']
            self.broadcast_port = 0 if self.broadcast_port == '' else int(self.broadcast_port)

            self.fund_trans_ip = logInfoMap['htm_server_list']['fund_trans_ip']
            self.fund_trans_port = logInfoMap['htm_server_list']['fund_trans_port']
            self.fund_trans_port = 0 if self.fund_trans_port == '' else int(self.fund_trans_port)

            self.query_ip = logInfoMap['htm_server_list']['query_ip']
            self.query_port = logInfoMap['htm_server_list']['query_port']
            self.query_port = 0 if self.query_port == '' else int(self.query_port)

            self.risk_broadcast_ip = logInfoMap['htm_server_list']['risk_broadcast_ip']
            self.risk_broadcast_port = logInfoMap['htm_server_list']['risk_broadcast_port']
            self.risk_broadcast_port = 0 if self.risk_broadcast_port == '' else int(self.risk_broadcast_port)

            self.risk_trans_ip = logInfoMap['htm_server_list']['risk_trans_ip']
            self.risk_trans_port = logInfoMap['htm_server_list']['risk_trans_port']
            self.risk_trans_port = 0 if self.risk_trans_port == '' else int(self.risk_trans_port)

            self.server_code = logInfoMap['htm_server_list']['server_code']
            self.server_name = logInfoMap['htm_server_list']['server_name']

            self.trans_ip = logInfoMap['htm_server_list']['trans_ip']
            self.trans_port = logInfoMap['htm_server_list']['trans_port']
            self.trans_port = 0 if self.trans_port == '' else int(self.trans_port)

            self.oper_flag = logInfoMap['oper_flag']
            self.rsp_msg = logInfoMap['rsp_msg']
            self.session_id = logInfoMap['session_id']
            self.session_key = logInfoMap['session_key']

    def toString(self):
        reStr = ''
        for k, v in vars(self).items():
            reStr = reStr + str(k) + '=' + str(v) + '\n'
        return reStr


'''返回客户信息的储存类'''


class CustomerInfo(RspBase):

    def __init__(self):
        self.rsp_msg = ''  # 处理结果
        self.oper_flag = 0  # 处理结果标记
        self.c_acct_no = ''  # 客户号
        self.c_cust_id = ''  # 客户号
        self.c_account_no = ''  # 银行账号
        self.c_open_bank_name = ''  # 开户银行名称
        self.c_cust_abbr = ''  # 客户名字
        self.c_b_fare_model_id = ''
        self.c_m_fare_model_id = ''
        self.c_acct_type = 0
        self.c_ocma_flag = 0
        self.c_acct_stat = 0
        self.c_cert_type = ''
        self.c_cert_num = ''  # 客户身份证号码
        self.c_branch_id = ''
        self.f_currency_id = 1
        self.f_curr_bal = 0
        self.f_can_use_bal = 0  # 可用资金
        self.f_can_get_bal = 0  # 可提资金
        self.f_in_bal = 0
        self.f_out_bal = 0
        self.f_buy_bal = 0
        self.f_sell_bal = 0
        self.f_exch_froz_bal = 0  # 交易冻结资金
        self.f_posi_margin = 0  # 持仓保证金
        self.f_base_margin = 0
        self.f_take_margin = 0
        self.f_stor_margin = 0
        self.f_pt_reserve = 0
        self.f_ag_margin = 0
        self.f_forward_froz = 0
        self.f_exch_fare = 0  # 手续费
        self.r_surplus = 0.00  # 浮动盈亏
        self.f_offset_quota = 0
        self.f_avaliable_offset_quota = 0
        self.f_used_offset_quota = 0
        self.f_offset_entr_margin = 0
        self.htm_td_info = []

    def fromString(self, CustStr):
        msgTuple = re.findall(r'(.*?)=(.*?)#', CustStr.split('#', 1)[1], re.M | re.I)
        CustInfoMap = {}
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
            self.c_acct_type = int(CustInfoMap['c_acct_type'])
            self.c_ocma_flag = int(CustInfoMap['c_ocma_flag'])
            self.c_acct_stat = int(CustInfoMap['c_acct_stat'])
            self.c_cert_type = CustInfoMap['c_cert_type']
            self.c_cert_num = CustInfoMap['c_cert_num']
            self.c_branch_id = CustInfoMap['c_branch_id']
            self.f_currency_id = int(CustInfoMap['f_currency_id'])
            self.f_curr_bal = float(CustInfoMap['f_curr_bal'])
            self.f_can_use_bal = float(CustInfoMap['f_can_use_bal'])
            self.f_can_get_bal = float(CustInfoMap['f_can_get_bal'])
            self.f_in_bal = float(CustInfoMap['f_in_bal'])
            self.f_out_bal = float(CustInfoMap['f_out_bal'])
            self.f_buy_bal = float(CustInfoMap['f_buy_bal'])
            self.f_sell_bal = float(CustInfoMap['f_sell_bal'])
            self.f_exch_froz_bal = float(CustInfoMap['f_exch_froz_bal'])
            self.f_posi_margin = float(CustInfoMap['f_posi_margin'])
            self.f_base_margin = float(CustInfoMap['f_base_margin'])
            self.f_take_margin = float(CustInfoMap['f_take_margin'])
            self.f_stor_margin = float(CustInfoMap['f_stor_margin'])
            self.f_pt_reserve = float(CustInfoMap['f_pt_reserve'])
            self.f_ag_margin = float(CustInfoMap['f_ag_margin'])
            self.f_forward_froz = float(CustInfoMap['f_forward_froz'])
            self.f_exch_fare = float(CustInfoMap['f_exch_fare'])
            self.r_surplus = float(CustInfoMap['r_surplus'])
            self.f_offset_quota = float(CustInfoMap['f_offset_quota'])
            self.f_avaliable_offset_quota = float(CustInfoMap['f_avaliable_offset_quota'])
            self.f_used_offset_quota = float(CustInfoMap['f_used_offset_quota'])
            self.f_offset_entr_margin = float(CustInfoMap['f_offset_entr_margin'])
            if 'htm_td_info' not in CustInfoMap:
                return
            htm_td_info = CustInfoMap['htm_td_info']
            self.htm_td_info = TDInfo.fromString(htm_td_info)

    def toDict(self):
        result = vars(self).copy()
        if result['htm_td_info'] == []:
            return result
        htm_td_info = []
        for item in result['htm_td_info']:
            htm_td_info.append(item.toDict())
        result['htm_td_info'] = htm_td_info
        return result


'''仓位情况类'''


class TDInfo(RspBase):
    def __init__(self):

        self.td_day_cov_long_froz = 0  # 当日平多仓冻结
        self.td_day_cov_short_froz = 0  # 当日平空仓冻结
        self.td_short_open_avg_price = 0.00  # 空头开仓均价
        self.td_long_amt = 0  # 当前多仓
        self.td_day_open_short = 0  # 当日开空仓
        self.td_day_deli_short = 0  # 当日交割空仓
        self.td_day_open_long = 0  # 当日开多仓
        self.td_day_deli_long_forz = 0  # 当日交割多仓冻结
        self.td_short_amt = 0  # 当前空仓
        self.td_day_cov_short = 0  # 当日平空仓
        self.td_day_settle_price = 0.00  # 当日结算价
        self.td_last_settle_price = 0.00  # 上日结算价
        self.td_long_posi_avg_price = 0.00  # 多头持仓均价
        self.td_can_use_short = 0  # 可用空仓
        self.td_long_margin = 0.00  # 多头持仓保证金
        self.td_long_open_avg_price = 0.00  # 多头开仓均价
        self.td_prod_code = ""  # 合约代码
        self.td_day_cov_long = 0  # 当日平多仓
        self.td_short_margin = 0.00  # 空头持仓保证金
        self.td_day_deli_long = 0  # 当日交割多仓
        self.td_day_deli_short_forz = 0  # 当日交割空仓冻结
        self.td_short_posi_avg_price = 0.00  # 空头持仓均价
        self.td_can_use_long = 0  # 可用多仓

    @staticmethod
    def fromString(infoStr):
        # td_day_cov_long_froz｜td_day_cov_short_froz｜td_short_open_avg_price｜td_long_amt｜td_day_open_short｜td_day_deli_short｜td_day_open_long｜td_day_deli_long_forz｜td_short_amt｜td_day_cov_short｜td_day_settle_price｜td_last_settle_price｜td_long_posi_avg_price｜td_can_use_short｜td_long_margin｜td_long_open_avg_price｜td_prod_code｜td_day_cov_long｜td_short_margin｜td_day_deli_long｜td_day_deli_short_forz｜td_short_posi_avg_price｜td_can_use_long｜∧0ˇ0ˇ0ˇ1ˇ0ˇ0ˇ1ˇ0ˇ0ˇ0ˇ0ˇ358.19ˇ356.93ˇ0ˇ2855.44ˇ356.93ˇmAu(T+D)ˇ0ˇ0ˇ0ˇ0ˇ0ˇ1ˇ｜∧
        result = []
        kv = infoStr.split('｜∧')
        if len(kv) < 3:
            return result;
        key = kv[0].split('｜')
        for v in kv[1:-1]:
            td = TDInfo()
            r = {}
            value = v.split('ˇ')
            r.update(zip(key, value))
            td.td_day_cov_long_froz = int(r['td_day_cov_long_froz'])  # 当日平多仓冻结
            td.td_day_cov_short_froz = int(r['td_day_cov_short_froz'])  # 当日平空仓冻结
            td.td_short_open_avg_price = float(r['td_short_open_avg_price'])  # 空头开仓均价
            td.td_long_amt = int(r['td_long_amt'])  # 当前多仓
            td.td_day_open_short = int(r['td_day_open_short'])  # 当日开空仓
            td.td_day_deli_short = int(r['td_day_deli_short'])  # 当日交割空仓
            td.td_day_open_long = int(r['td_day_open_long'])  # 当日开多仓
            td.td_day_deli_long_forz = int(r['td_day_deli_long_forz'])  # 当日交割多仓冻结
            td.td_short_amt = int(r['td_short_amt'])  # 当前空仓
            td.td_day_cov_short = int(r['td_day_cov_short'])  # 当日平空仓
            td.td_day_settle_price = float(r['td_day_settle_price'])  # 当日结算价
            td.td_last_settle_price = float(r['td_last_settle_price'])  # 上日结算价
            td.td_long_posi_avg_price = float(r['td_long_posi_avg_price'])  # 多头持仓均价
            td.td_can_use_short = int(r['td_can_use_short'])  # 可用空仓
            td.td_long_margin = float(r['td_long_margin'])  # 多头持仓保证金
            td.td_long_open_avg_price = float(r['td_long_open_avg_price'])  # 多头开仓均价
            td.td_prod_code = r['td_prod_code']  # 合约代码
            td.td_day_cov_long = int(r['td_day_cov_long'])  # 当日平多仓
            td.td_short_margin = float(r['td_short_margin'])  # 空头持仓保证金
            td.td_day_deli_long = int(r['td_day_deli_long'])  # 当日交割多仓
            td.td_day_deli_short_forz = int(r['td_day_deli_short_forz'])  # 当日交割空仓冻结
            td.td_short_posi_avg_price = float(r['td_short_posi_avg_price'])  # 空头持仓均价
            td.td_can_use_long = int(r['td_can_use_long'])  # 可用多仓
            result.append(td)
        return result


'''返回行情信息单项类'''


class QuoteItem(RspBase):
    def __init__(self):
        self.ApiName = ''
        self.RspMsg = ''
        self.instID = ''
        self.quoteDate = ''
        self.RspCode = ''
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

    def fromDict(self, qDict):
        for k in qDict.keys():
            v = qDict[k]
            if k == 'sZipBuff':
                for kk in v.keys():
                    vv = qDict[k][kk]
                    if kk == 'quoteTime':
                        exec('self.' + kk + '=vv')
                    else:
                        exec('self.' + kk + '=float(vv)')
            else:
                exec('self.' + k + '=v')
        return


'''返回行情信息类'''


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

    def fromDict(self, qDict):
        if 'instID' in qDict:
            key = qDict['instID']
            exec('self.' + re.sub('[.+()]', '', key).lower() + '.fromDict(qDict)')
        return


'''获取交易信息单项类(提供字段名称 及获取信息)'''


class Alm_View_item(object):
    def __init__(self):
        self.exch_date = ''  # 交易日期 20190827
        self.order_no = ''  # 报单号  02105393
        self.market_id = ''  # 市场编号 02
        self.prod_code = ''  # 合约代码 Ag(T+D)
        self.exch_code = ''  # 交易类型 4041
        self.entr_price = 0  # 委托价格 4280
        self.entr_amount = 0  # 委托数量 1
        self.remain_amount = 0  # 未成交数量 1
        self.offset_flag = ''  # 平仓标志（对冲） （1：是 0：否）
        self.entr_stat = ''  # 交易状态 o（开）c(卖) d(撤销)
        self.e_term_type = ''  # ? 03
        self.e_exch_time = ''  # 委托时间 214158
        self.c_term_type = ''  # ? ''
        self.c_exch_time = ''  # 成交时间  215742
        self.rsp_msg = ''  # 回复信息  处理成功
        self.local_order_no = ''  # 本地报单号 100993

    def fromString(self, infoStr):
        result = infoStr.split('｜')
        self.exch_date = result[0]
        self.order_no = result[1]
        self.market_id = result[2]
        self.prod_code = result[3]
        self.exch_code = result[4]
        self.entr_price = float(result[5])
        self.entr_amount = int(result[6])
        self.remain_amount = int(result[7])
        self.offset_flag = result[8]
        self.entr_stat = result[9]
        self.e_term_type = result[10]
        self.e_exch_time = result[11]
        self.c_term_type = result[12]
        self.c_exch_time = result[13]
        self.rsp_msg = result[14]
        self.local_order_no = result[15]

    def toDict(self):
        return vars(self)


'''获取交易信息汇总类'''


class Alm_View(object):
    def __init__(self):
        self.curr_page = 0
        self.oper_flag = 0
        self.page_count = 0
        self.paginal_num = 0
        self.rsp_msg = ''

        self.average_price = 0
        self.entr_amount = 0
        self.remain_amount = 0
        self.billList = []

    def fromString(self, infoStr):
        reList = re.findall(r'(?<=#)(.*?)=(.*?)#', infoStr, re.M | re.I | re.S)
        reDict = {}
        reDict.update(reList)
        if reDict['oper_flag'] == '0':
            return False, reDict['rsp_msg']
        self.rsp_msg = reDict['rsp_msg']
        self.oper_flag = int(reDict['oper_flag'])
        self.paginal_num = int(reDict['paginal_num'])
        self.curr_page = int(reDict['curr_page'])
        alm_result_str = reDict['alm_result']
        alm_result_list = alm_result_str.split('∧')
        totle_result = alm_result_list[-2].split('｜')
        if totle_result[0] != '合计':
            return False, "统计信息有误" + alm_result_list[-2]
        self.average_price = 0 if totle_result[5] == '' else float(totle_result[5])
        self.entr_amount = 0 if totle_result[6] == '' else int(totle_result[6])
        self.remain_amount = 0 if totle_result[7] == '' else int(totle_result[7])
        self.billList = []
        if len(alm_result_list) == 2:
            return True, "Totle:0"
        alm_result_item_list = alm_result_list[0:-2]
        for item in alm_result_item_list:
            alm_view_item = Alm_View_item()
            alm_view_item.fromString(item)
            self.billList.append(alm_view_item)

    def toDict(self):
        reDict = vars(self).copy()
        if len(self.billList) == 0:
            return reDict
        reDict['billList'] = []
        for item in self.billList:
            reDict['billList'].append(item.toDict())
        return reDict
