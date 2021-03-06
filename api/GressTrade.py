import api.Trans as Trans 
import api.Comm as Comm
from api.config import *
import socket, re, gzip
import pprint
import datetime,time
import base64


class API():
    '''初始化'''

    def __init__(self):
        self.serverInfo = Trans.ServerInfo()
        self.custInfo = Trans.CustomerInfo()
        self.user_id = ''
        self.__user_pwd = ''
        self.quote = Trans.Quote()
        socket.setdefaulttimeout(2)
        self.quoteClient=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    '''登陆'''

    def login(self, username, password):
        # 数据头
        GReqHead = Trans.ReqHead()
        GReqHead.exch_code = '8006'
        GReqHead.msg_type = '1'
        GReqHead.msg_flag = '1'
        GReqHead.term_type = '03'
        GReqHead.user_type = '2'
        GReqHead.user_id = username
        self.serverInfo.user_id = username
        # 数据体
        v_reqMag = Trans.ReqT8006()
        v_reqMag.bank_no = Constant['bank_no']
        v_reqMag.login_ip = Constant['login_ip']
        v_reqMag.net_agent = '1'
        v_reqMag.net_envionment = '2'
        v_reqMag.oper_flag = '1'
        v_reqMag.user_id = username
        v_reqMag.user_id_type = '1'
        v_reqMag.user_pwd = Comm.MD5(password)
        v_reqMag.user_type = '2'
        # 数据头+数据体
        v_sMsg = GReqHead.toString() + v_reqMag.toString()

        self.user_id = v_reqMag.user_id
        self.__user_pwd = v_reqMag.user_pwd
        publicKey = Comm.getCrtFilePublickey("./api/cert/server.crt")
        buffer = ''.encode('utf-8')
        for i in range(0, len(v_sMsg), 100):
            buffer = buffer + Comm.rsaEncrypt(v_sMsg[i:i + 100].encode('utf-8'), publicKey)
        buffer_Len_Str = Comm.Fill(str(len(buffer)), '0', 8, 'L')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log_ip = Constant['log_server_ip']
        log_port = Constant['log_server_port']
        client.connect((log_ip, log_port))
        client.send(buffer_Len_Str.encode('utf-8'))
        client.send(buffer)
        buffer4 = client.recv(8)
        buffer5 = client.recv(int(buffer4.decode('utf-8')))
        client.close()
        privateKey = Comm.getPfxFilePrivatekey("./api/cert/client.pfx", '123456')
        streamArr = ''.encode('utf-8')
        for i in range(0, len(buffer5), 128):
            buffer6 = buffer5[i:i + 128]
            streamArr = streamArr + Comm.rsaDecrypt(buffer6, privateKey)
        logSevStr = streamArr.decode('gbk')
        self.serverInfo.fromString(logSevStr)
        if self.serverInfo.rsp_msg == '处理成功':
            return True, "登陆成功"
        else:
            return False, self.serverInfo.rsp_msg

    '''获取客户账户信息'''

    def getCustInfo(self):
        # 数据头
        GReqHead = Trans.ReqHead()
        GReqHead.branch_id = self.serverInfo.branch_id
        GReqHead.exch_code = '1020'
        GReqHead.msg_flag = '1'
        GReqHead.msg_type = '1'
        GReqHead.term_type = '03'
        GReqHead.user_id = self.serverInfo.user_id
        GReqHead.user_type = '2'
        # 数据体
        v_reqMag = Trans.ReqT1020()
        v_reqMag.acct_no = self.serverInfo.user_id
        v_reqMag.is_check_stat = '1'
        v_reqMag.oper_flag = '1'
        v_reqMag.oper_flag = '1'
        v_reqMag.qry_cust_info = '1'
        v_reqMag.qry_defer = '1'
        v_reqMag.qry_forward = '1'
        v_reqMag.qry_fund = '1'
        v_reqMag.qry_storage = '1'
        v_reqMag.qry_surplus = '1'
        v_sMsg = GReqHead.toString() + v_reqMag.toString()
        ip = self.serverInfo.trans_ip
        port = self.serverInfo.trans_port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.__SendGoldMsg(client, v_sMsg)
        customInfo_str = self.__RecvGoldMsg(client)
        client.close()
        self.custInfo.fromString(customInfo_str)
        return self.custInfo.toDict()

    '''获取报价'''

    def getQuote(self):
        # 数据体
        v_reqMag = Trans.GBcMsgReqLink()
        v_reqMag.RspCode = ''
        v_reqMag.RspMsg = ''
        v_reqMag.again_flag = '0'
        v_reqMag.branch_id = self.serverInfo.branch_id
        v_reqMag.cust_type_id = 'C01'
        v_reqMag.is_lfv = '1'
        v_reqMag.lan_ip = Constant['login_ip']
        v_reqMag.term_type = ''
        v_reqMag.user_id = self.user_id
        v_reqMag.user_key = datetime.datetime.now().strftime('%H%M%S%f')[0:-3]
        v_reqMag.user_pwd = self.__user_pwd
        v_reqMag.user_type = Constant['user_type']
        v_reqMag.www_ip = ''

        v_sMsg = v_reqMag.toString()
        ip = self.serverInfo.broadcast_ip
        port = self.serverInfo.broadcast_port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.__SendGoldMsg(client, v_sMsg)
        for i in range(52):
            QuoteInfo_Dict = self.__RecvGoldMsg(client)
            self.quote.fromDict(QuoteInfo_Dict)
        client.close()

    def getQuote2(self):
      # 非交易时间段只进行一次价格查询
      if  Comm.isTradeTime()!=1:
          self.getQuote_start()
          self.quoteClient.shutdown((socket.SHUT_RDWR))
          print('非交易时间段只进行一次价格查询')
          return
      # 交易时间段内最多重新连接5次
      i=0
      while i<5:
            try:
                self.getQuote_step()
                print('价格轮询成功')
                return
            except socket.timeout:
                print('超时,重新建立连接...(%d)'%(i+1))
                self.getQuote_start()
                i+=1
            except socket.os.error:
                print('socket无效,重新建立连接...(%d)'%(i+1))
                i+=1
                self.getQuote_start()
      self.quoteClient.shutdown((socket.SHUT_RDWR))
      print('行情服务器关闭！')


    '''获取报价（建立连接并接受首批数据）'''

    def getQuote_start(self):
        # 数据体
        v_reqMag = Trans.GBcMsgReqLink()
        v_reqMag.RspCode = ''
        v_reqMag.RspMsg = ''
        v_reqMag.again_flag = '0'
        v_reqMag.branch_id = self.serverInfo.branch_id
        v_reqMag.cust_type_id = 'C01'
        v_reqMag.is_lfv = '1'
        v_reqMag.lan_ip = Constant['login_ip']
        v_reqMag.term_type = ''
        v_reqMag.user_id = self.user_id
        v_reqMag.user_key = datetime.datetime.now().strftime('%H%M%S%f')[0:-3]
        v_reqMag.user_pwd = self.__user_pwd
        v_reqMag.user_type = Constant['user_type']
        v_reqMag.www_ip = ''

        v_sMsg = v_reqMag.toString()
        ip = self.serverInfo.broadcast_ip
        port = self.serverInfo.broadcast_port
        #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
           self.quoteClient.shutdown((socket.SHUT_RDWR))
        except:
           pass
        self.quoteClient=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client=self.quoteClient
        
        client.connect((ip, port))
        self.__SendGoldMsg(client, v_sMsg)
        for i in range(48): #?????????????到超时结束，行情表弟有时会有改变，怎么确定？
            self.getQuote_step()
        #client.close()

    '''单步获取行情，用于价格轮询'''

    def getQuote_step(self):
        client=self.quoteClient
        QuoteInfo_Dict = self.__RecvGoldMsg(client)
        self.quote.fromDict(QuoteInfo_Dict)

        #pprint.pprint(QuoteInfo_Dict)
        #print('--------------------------------------------')      

    '''交易函数 '''

    def trade(self, code, bs, price, amount):
        '''
         交易方向 4041(开多) 4042（开空） 4043（平多） 4044（平空）
        '''
        if code not in CodeList:
            return False, "交易对象" + code + "不在列表中"
        if bs == 'ob':
            exch_code = '4041'
            v_reqMag = Trans.ReqT4041()
        elif bs == 'os':
            exch_code = '4042'
            v_reqMag = Trans.ReqT4042()
        elif bs == 'cb':
            exch_code = '4043'
            v_reqMag = Trans.ReqT4043()
        elif bs == 'cs':
            exch_code = '4044'
            v_reqMag = Trans.ReqT4044()
        else:
            return False, "交易方向错误，应为ob(开多),os(开空),cb(平多),cs(平空)中的一种"

        # 数据头
        GReqHead = Trans.ReqHead()
        GReqHead.branch_id = self.serverInfo.branch_id
        GReqHead.exch_code = exch_code
        GReqHead.msg_flag = '1'
        GReqHead.msg_type = '1'
        GReqHead.term_type = '03'
        GReqHead.user_id = self.serverInfo.user_id
        GReqHead.user_type = '2'
        # 数据体
        v_reqMag.acct_no = self.serverInfo.user_id
        v_reqMag.client_serial_no = self.serverInfo.user_id + str((
                                                                              datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second) * 10)  # '1021805322584010'
        v_reqMag.cust_id = self.serverInfo.user_id
        v_reqMag.entr_amount = amount  # 交易数量
        v_reqMag.entr_price = price  # 交易价格
        v_reqMag.prod_code = code  # 交易品种

        v_sMsg = GReqHead.toString() + v_reqMag.toString()
        ip = self.serverInfo.trans_ip
        port = self.serverInfo.trans_port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.__SendGoldMsg(client, v_sMsg)
        trade_Dict = Comm.splitInfoStr(self.__RecvGoldMsg(client))
        print(trade_Dict)
        client.close()
        

    '''撤单函数 '''

    def cancel(self, order_no):
        # 数据头
        GReqHead = Trans.ReqHead()
        GReqHead.branch_id = self.serverInfo.branch_id
        GReqHead.exch_code = '4061'
        GReqHead.msg_flag = '1'
        GReqHead.msg_type = '1'
        GReqHead.term_type = '03'
        GReqHead.user_id = self.serverInfo.user_id
        GReqHead.user_type = '2'
        # 数据体
        v_reqMag = Trans.ReqT4061()
        v_reqMag.cancel_order_no = order_no
        v_reqMag.oper_flag = 1
        v_sMsg = GReqHead.toString() + v_reqMag.toString()
        ip = self.serverInfo.trans_ip
        port = self.serverInfo.trans_port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.__SendGoldMsg(client, v_sMsg)
        trade_Dict = Comm.splitInfoStr(self.__RecvGoldMsg(client))
        print(trade_Dict)
        client.close()

    '''交易信息查询'''

    def getTradeInfo(self):
        # 数据头
        GReqHead = Trans.ReqHead()
        GReqHead.branch_id = self.serverInfo.branch_id
        GReqHead.exch_code = '6002'
        GReqHead.msg_flag = '1'
        GReqHead.msg_type = '1'
        GReqHead.term_type = '03'
        GReqHead.user_id = self.serverInfo.user_id
        GReqHead.user_type = '2'
        # 数据体
        v_reqMag = Trans.ReqT6002()
        v_reqMag.alm_view_field = '∧'.join(list(vars(Trans.Alm_View_item()).keys()))
        # v_reqMag.alm_view_field="exch_date∧order_no∧market_id∧prod_code∧exch_code∧entr_price∧entr_amount∧remain_amount∧offset_flag∧entr_stat∧e_term_type∧e_exch_time∧c_term_type∧c_exch_time∧rsp_msg∧local_order_no∧"
        v_reqMag.curr_page = '1'
        v_reqMag.login_branch_id = self.serverInfo.branch_id
        v_reqMag.login_teller_id = self.serverInfo.user_id
        v_reqMag.oper_flag = '1'
        v_reqMag.paginal_num = '500'
        v_reqMag.query_id = 'AcctEntrFlow'

        v_sMsg = GReqHead.toString() + v_reqMag.toString()
        # 'cb8e8527160021032 1021805322    B00151853                       #alm_view_field=exch_date∧order_no∧market_id∧prod_code∧exch_code∧entr_price∧entr_amount∧remain_amount∧offset_flag∧entr_stat∧e_term_type∧e_exch_time∧c_term_type∧c_exch_time∧rsp_msg∧local_order_no∧#curr_page=1#login_branch_id=B00151853#login_teller_id=1021805322#oper_flag=1#paginal_num=500#query_id=AcctEntrFlow#prod_code=#exch_code=#b_offset_flag=#'
        ip = self.serverInfo.query_ip
        port = self.serverInfo.query_port

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.__SendGoldMsg(client, v_sMsg)
        tradeInfo_str = self.__RecvGoldMsg(client)
        client.close()
        alm_view = Trans.Alm_View()
        alm_view.fromString(tradeInfo_str)
        return alm_view.toDict()

    '''关闭'''

    def Close(self):
        try:
          self.quoteClient.shutdown(socket.SHUT_RDWR)# 关闭行情接受客户端
        except Exception:
            pass
        # 数据头
        GReqHead = Trans.ReqHead()
        GReqHead.branch_id = self.serverInfo.branch_id
        GReqHead.exch_code = '8002'
        GReqHead.msg_flag = '1'
        GReqHead.msg_type = '1'
        GReqHead.term_type = '03'
        GReqHead.user_id = self.serverInfo.user_id
        GReqHead.user_type = '2'
        # 数据体
        v_reqMag = Trans.ReqT8002()
        v_reqMag.oper_flag = '1'
        v_reqMag.user_id = self.serverInfo.user_id
        v_reqMag.user_type = '2'

        v_sMsg = GReqHead.toString() + v_reqMag.toString()
        ip = self.serverInfo.trans_ip
        port = self.serverInfo.trans_port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.__SendGoldMsg(client, v_sMsg)
        close_str = self.__RecvGoldMsg(client)
        client.close()
        closeR = re.findall(r'rsp_msg=(.*?)#', close_str, re.M | re.I)[0]
        if closeR == '处理成功':
            print('关闭成功')
            return (True, closeR)
        print('关闭失败')
        return (False, closeR)


        # fb9e673180022032 1021805322    B00151853   00000000#rsp_msg=处理成功#oper_flag=1#

    '''发送函数'''

    def __SendGoldMsg(self, client, v_sMsg):
        # v_sMsg=Comm.Fill(str(len(v_sMsg)),'0',8,'L')+v_sMsg
        v_sMsg = Comm.Fill(str(len(v_sMsg.encode('gbk'))), '0', 8, 'L') + v_sMsg
        v_sMsg = v_sMsg.encode('gbk')

        buffer = self.__TripleDes_encryptMsg(2, v_sMsg)
        client.send(buffer)

    '''接受函数'''

    def __RecvGoldMsg(self, client):
        num = int(self.__RecvByLen(client, 8).decode('utf-8'))
        vReadBytes = self.__RecvByLen(client, num)
        arrLfvMsg = self.__TripleDes_decryptMsg(self.__unzipReadBytes(vReadBytes))
        if len(arrLfvMsg) > 8 and arrLfvMsg[0] == 35 and arrLfvMsg[1] == 76 and arrLfvMsg[2] == 102 and arrLfvMsg[
            3] == 118 and arrLfvMsg[4] == 77 and arrLfvMsg[5] == 115 and arrLfvMsg[6] == 103 and arrLfvMsg[7] == 61:
            str = self.__GlobalLfvTransfer_lfvToKv(arrLfvMsg, 8, len(arrLfvMsg) - 2)
        else:
            str = arrLfvMsg.decode('gbk')
        return str

    '''按长度接受数据'''

    def __RecvByLen(self, client, v_iRecvLen):
        num = 0
        buffer = ''.encode('utf-8');
        while num < v_iRecvLen:
            size = v_iRecvLen - num;
            if size > 1024:
                size = 1024;
            buffer2 = client.recv(size)
            num3 = len(buffer2)
            if num3 > 0:
                buffer = buffer + buffer2
                num = num + num3
            else:
                client.close()
                raise '无数据，可能被远程主机强制关闭'
        return buffer

    '''3DS加密'''

    def __TripleDes_encryptMsg(self, i__encryptMode, bSrcMsgBuff):
        if i__encryptMode == 2 or i__encryptMode == 3:
            SESSION_KEY = '240262447423713749922240'
        if i__encryptMode == 3 and self.serverInfo.session_key != '':
            SESSION_KEY = self.serverInfo.session_key
        IV_DEFAULT = '12345678'
        sourceArray = self.__encrypt(SESSION_KEY, IV_DEFAULT, bSrcMsgBuff);
        destinationArray_len = 8 + 1 + 10 + len(sourceArray)
        destinationArray = Comm.Fill(str(destinationArray_len - 8), '0', 8, 'L').encode('utf-8') + bytes(
            [i__encryptMode]) + Comm.Fill(self.serverInfo.session_id, '0', 10, 'R').encode('utf-8') + sourceArray
        return destinationArray

    '''3DS加密实现'''

    def __encrypt(self, key, iv, value):
        return Comm.triple_des_encrypt(key, iv, value)

    '''3DS解密'''

    def __TripleDes_decryptMsg(self, bDecryptMsgBuff):
        __encrypt_MODEL_LEN = 1
        SESSION_LEN = 10;
        IV_DEFAULT = '12345678';
        num = bDecryptMsgBuff[__encrypt_MODEL_LEN - 1];
        if num == 1:
            pass
        elif num == 2:
            key = '240262447423713749922240'
            vStartIndex = __encrypt_MODEL_LEN + SESSION_LEN
            buffer = bDecryptMsgBuff[vStartIndex:]
            vSrcBuff = self.__decrypt(key, IV_DEFAULT, buffer)
            return vSrcBuff[9:]
        return bDecryptMsgBuff

    '''3DS解密实现'''

    def __decrypt(self, key, iv, value):
        return Comm.triple_des_decrypt(key, iv, value)

    '''解压缩数据gzip '''

    def __unzipReadBytes(self, vReadBytes):
        if len(vReadBytes) > 1 and vReadBytes[0] == 1:
            bytes = vReadBytes[1:];
            buffer2 = gzip.decompress(bytes)
            arrLfvMsg = buffer2[9:]
        else:
            arrLfvMsg = vReadBytes
        return arrLfvMsg

    '''报价数据分解 '''

    def __GlobalLfvTransfer_lfvToKv(self, arrLfvMsg, iStartIndex, iEndIndex):
        strDict = {}
        iOffset = iStartIndex
        while iOffset <= iEndIndex:
            num2 = self.__byteToInt(arrLfvMsg, iOffset, 2)
            iOffset = iOffset + 2;
            idx = self.__byteToInt(arrLfvMsg, iOffset, 2)
            iOffset = iOffset + 2;
            str1 = arrLfvMsg[iOffset: iOffset + num2 - 2]
            iOffset = iOffset + num2 - 2
            #print(idx)
            name = FieldName[idx]
            value = str1.decode('gbk')
            if name == 'sZipBuff':
                value = self.__unzipQuote(value)
            strDict[name] = value
        return strDict

    '''byte数据转int'''

    def __byteToInt(self, arrLfvMsg, iOffset, iLen):
        num = 0;
        for i in range(iOffset, iOffset + iLen, 1):
            num += (arrLfvMsg[i] & 0xff) << (8 * ((iLen - 1) - (i - iOffset)))
        return num

    '''报价字符串解码'''

    def __unzipQuote(self, sZipBuff):
        strDict = {}
        mNeedZipFields = ['lastSettle', 'lastClose', 'open', 'high', 'low', 'last', 'close', 'settle', 'bid1',
                          'bidLot1', 'bid2', 'bidLot2', 'bid3', 'bidLot3', 'bid4', 'bidLot4',
                          'bid5', 'bidLot5', 'ask1', 'askLot1', 'ask2', 'askLot2', 'ask3', 'askLot3', 'ask4', 'askLot4',
                          'ask5', 'askLot5', 'volume', 'weight', 'highLimit', 'lowLimit',
                          'Posi', 'upDown', 'turnOver', 'average', 'sequenceNo', 'quoteTime', 'upDownRate']
        buffer = base64.b64decode(sZipBuff)
        i = 0;
        while i < len(buffer):
            num2 = buffer[i]
            strbin = Comm.Fill(bin(num2)[2:], '0', 8, 'L')
            if len(strbin) > 8:
                strbin = strbin[-8:]
            index = int('0b' + strbin[0:6], 2)
            num4 = 3 + int('0b' + strbin[6:], 2);
            if i >= len(buffer) - 1:
                break
            bytes = buffer[i + 1:i + num4 + 1]
            i = i + num4 + 1
            name = mNeedZipFields[index]

            value = self.__toLongByBytes(bytes) / 1000
            # value=value/1000
            if name == 'quoteTime':
                value = Comm.Fill(str(int(value * 1000)), '0', 6, 'L')
                if len(value) == 6:
                    value = value[0:2] + ':' + value[2:4] + ':' + value[4:]
            if name == 'upDownRate':
                value = value / 10000

            strDict[name] = value
        return strDict

    '''bytes转long'''

    def __toLongByBytes(self, bytes):
        strR = ''
        for i in range(len(bytes)):
            str2 = format(bytes[i], '#010b')[2:]
            if len(str2) > 8:
                str2 = str2[-8:] #可能有错
            strR = strR + str2
        if strR[0] == '1':
            return int('0b0' + strR[1:], 2) * (-1)
        return int('0b' + strR, 2)
