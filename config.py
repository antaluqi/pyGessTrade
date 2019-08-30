# -*- coding: gb2312 -*-

import socket
'''
全局配置
'''

'''商品代码列表'''
CodeList=['Au99.99','Au100g','iAu99.99','Au50g','iAu100g','Au99.95',\
          'Au(T+N2)','Ag(T+D)','Au(T+N1)','Au(T+D)','Ag99.99','Au99.5',\
          'Ag99.9','PGC30g','iAu99.5','Pt99.95','mAu(T+D)']

'''一些基础配置数据'''
Constant={
    'bank_no':'0015',
    'login_ip':socket.gethostbyname(socket.gethostname(  )),
    'net_agent':'1',
    'net_envionment':'2',
    'oper_flag':'1',
    'user_id_type':'1',
    'user_pwd':'',
    'user_type':'2',
    'SEQ_NO':0,
    'log_server_ip':'119.145.36.50',
    'log_server_port':20443,

}


'''字段代码对照表'''
FieldName={
    31 :'ApiName',
    49 : 'RspCode',
    54 : 'Ts_NodeID',
    650 : 'instID',
    1170 :'state',
    785 : 'marketID',
    786 : 'marketState',
    48 : 'RootID',
    50 : 'RspMsg',
    483: 'effectDate',
    549: 'feeRate',
    1086: 'sys_date  ',
    504: 'exch_date',
    773 :'m_sys_stat',
    253 : 'b_sys_stat',
    951: 'quoteDate',
    1006 : 'sZipBuff',
}

