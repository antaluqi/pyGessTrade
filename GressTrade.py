import Trans,Comm
from config import *
import socket,re,gzip
import pprint

class API():
    '''
    初始化
    '''
    def __init__(self):
        self.serverInfo=Trans.ServerInfo()
        self.custInfo=Trans.CustomerInfo()

    '''
    登陆
    '''
    def login(self,username,password):
        # 数据头
        GReqHead=Trans.ReqHead()
        GReqHead.exch_code='8006'
        GReqHead.msg_type='1'
        GReqHead.msg_flag='1'
        GReqHead.term_type='03'
        GReqHead.user_type='2'
        GReqHead.user_id=username
        self.serverInfo.user_id=username
        # 数据体
        v_reqMag=Trans.ReqT8006()
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
        v_sMsg=GReqHead.ToString()+v_reqMag.ToString()

        publicKey=Comm.getCrtFilePublickey("./cert/server.crt")
        buffer=''.encode('utf-8')
        for i in range(0,len(v_sMsg),100):
            buffer=buffer+Comm.rsaEncrypt(v_sMsg[i:i+100].encode('utf-8'),publicKey)
        buffer_Len_Str=Comm.Fill(str(len(buffer)),'0',8,'L')
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        log_ip=Constant['log_server_ip']
        log_port=Constant['log_server_port']
        client.connect((log_ip,log_port))
        client.send(buffer_Len_Str.encode('utf-8'))
        client.send(buffer)
        buffer4 = client.recv(8)
        buffer5=client.recv(int(buffer4.decode('utf-8')))
        client.close()
        privateKey=Comm.getPfxFilePrivatekey("./cert/client.pfx",'123456')
        streamArr=''.encode('utf-8')
        for i in range(0,len(buffer5),128):
            buffer6=buffer5[i:i+128]
            streamArr=streamArr+Comm.rsaDecrypt(buffer6,privateKey)
        logSevStr=streamArr.decode('gbk')
        self.serverInfo.fromString(logSevStr)
        if self.serverInfo.rsp_msg=='处理成功':
            return True,self.serverInfo.rsp_msg
        else:
            return  False,self.serverInfo.rsp_msg

    '''
    获取客户账户信息
    '''
    def getCustInfo(self):
        # 数据头
        GReqHead = Trans.ReqHead()
        GReqHead.branch_id=self.serverInfo.branch_id
        GReqHead.exch_code='1020'
        GReqHead.msg_flag='1'
        GReqHead.msg_type='1'
        GReqHead.term_type='03'
        GReqHead.user_id=self.serverInfo.user_id
        GReqHead.user_type='2'
        # 数据体
        v_reqMag=Trans.ReqT1020()
        v_reqMag.acct_no=self.serverInfo.user_id
        v_reqMag.is_check_stat='1'
        v_reqMag.oper_flag='1'
        v_reqMag.oper_flag='1'
        v_reqMag.qry_cust_info='1'
        v_reqMag.qry_defer='1'
        v_reqMag.qry_forward='1'
        v_reqMag.qry_fund='1'
        v_reqMag.qry_storage='1'
        v_reqMag.qry_surplus='1'
        v_sMsg = GReqHead.ToString() + v_reqMag.ToString()
        ip=self.serverInfo.trans_ip
        port=self.serverInfo.trans_port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.SendGoldMsg(client,v_sMsg)
        customInfo_str=self.RecvGoldMsg(client)
        client.close()
        self.custInfo.fromString(customInfo_str)

    '''
    获取报价
    '''
    def getQuote(self):
        # 数据体
        v_reqMag=Trans.GBcMsgReqLink()
        v_reqMag.RspCode = ''
        v_reqMag.RspMsg = ''
        v_reqMag.again_flag = '0'
        v_reqMag.branch_id = obj.ServerInfo.branch_id
        v_reqMag.cust_type_id = 'C01'
        v_reqMag.is_lfv = '1'
        v_reqMag.lan_ip = obj.login_ip
        v_reqMag.term_type = ''
        v_reqMag.user_id = obj.user_id
        v_reqMag.user_key = datestr(now, 'HHMMSSFFF')
        v_reqMag.user_pwd = obj.user_pwd
        v_reqMag.user_type = obj.user_type
        v_reqMag.www_ip = ''

    '''
    发送函数
    '''
    def SendGoldMsg(self,client,v_sMsg):
        v_sMsg=Comm.Fill(str(len(v_sMsg)),'0',8,'L')+v_sMsg
        buffer = self.TripleDes_encryptMsg(2, v_sMsg)
        client.send(buffer)

    '''
    接受函数
    '''
    def RecvGoldMsg(self,client):
        num=int(self.RecvByLen(client,8).decode('utf-8'))
        vReadBytes=self.RecvByLen(client,num)
        arrLfvMsg=self.TripleDes_decryptMsg(self.unzipReadBytes(vReadBytes))
        if len(arrLfvMsg) > 8 and arrLfvMsg[0] == 35 and arrLfvMsg[1] == 76 and arrLfvMsg[2] == 102 and arrLfvMsg[3] == 118 and arrLfvMsg[4] == 77 and arrLfvMsg[5] == 115 and arrLfvMsg[6] == 103 and arrLfvMsg[7] == 61:
            client.close()
            raise 'GlobalLfvTransfer_lfvToKv 函数'
        else:
            str=arrLfvMsg.decode('gbk')
        return str

    '''
    按长度接受数据
    '''
    def RecvByLen(obj,client,v_iRecvLen):
        num = 0
        buffer = ''.encode('utf-8');
        while num < v_iRecvLen:
            size = v_iRecvLen - num;
            if size > 1024:
                size = 1024;
            buffer2=client.recv(size)
            num3=len(buffer2)
            if num3>0:
                buffer=buffer+buffer2
                num=num+num3
            else:
                client.close()
                raise '无数据，可能被远程主机强制关闭'
        return buffer

    '''
    3DS加密
    '''
    def TripleDes_encryptMsg(self,iEncryptMode,bSrcMsgBuff):
        if iEncryptMode==2 or iEncryptMode==3:
            SESSION_KEY = '240262447423713749922240'
        if iEncryptMode==3 and self.serverInfo.session_key!='':
            SESSION_KEY = self.serverInfo.session_key
        IV_DEFAULT = '12345678'
        sourceArray = self.encrypt(SESSION_KEY, IV_DEFAULT, bSrcMsgBuff);
        destinationArray_len=8+1+10+len(sourceArray)
        destinationArray=Comm.Fill(str(destinationArray_len-8),'0',8,'L').encode('utf-8')+bytes([iEncryptMode])+Comm.Fill(self.serverInfo.session_id,'0',10,'R').encode('utf-8')+sourceArray
        return destinationArray


    '''
    3DS加密实现
    '''
    def encrypt(self,key,iv,value):
        return Comm.triple_des_encrypt(key,iv,value)


    '''
    3DS解密
    '''
    def TripleDes_decryptMsg(self,bDecryptMsgBuff):
        ENCRYPT_MODEL_LEN = 1
        SESSION_LEN = 10;
        IV_DEFAULT = '12345678';
        num = bDecryptMsgBuff[ENCRYPT_MODEL_LEN];
        if num==1:
            pass
        elif num==2:
            key = '240262447423713749922240'
            vStartIndex = ENCRYPT_MODEL_LEN + SESSION_LEN
            buffer = bDecryptMsgBuff[vStartIndex:]
            vSrcBuff = self.decrypt(key, IV_DEFAULT, buffer)
            return vSrcBuff[9:end]
        return bDecryptMsgBuff

    '''
    3DS解密实现
    '''
    def decrypt(self,key,iv,value):
        return Comm.triple_des_decrypt(key, iv, value)

    '''
    解压缩数据gzip
    '''
    def unzipReadBytes(obj, vReadBytes):
        if len(vReadBytes) > 1 and vReadBytes[0] == 1:
            bytes = vReadBytes[1:];
            buffer2=gzip.decompress(bytes)
            arrLfvMsg=buffer2[9:]
        else:
            arrLfvMsg=vReadBytes
        return arrLfvMsg









