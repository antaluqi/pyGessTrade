import Req,Comm
from config import *
import socket

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

        publicKey=Comm.getCrtFilePublickey("./cert/server.crt")
        buffer=''.encode('utf-8')
        for i in range(0,len(sMsg),100):
            buffer=buffer+Comm.rsaEncrypt(sMsg[i:i+100].encode('utf-8'),publicKey)
        buffer_Len_Str=Comm.Fill(str(len(buffer)),'0',8,'L')
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(('119.145.36.50',20443))
        client.send(buffer_Len_Str.encode('utf-8'))
        client.send(buffer)
        buffer4 = client.recv(8)
        buffer5=client.recv(int(buffer4.decode('utf-8')))
        client.close()
        privateKey=Comm.getPfxFilePrivatekey("./cert/client.pfx",'123456')
        streamArr=''.encode('utf-8')
        for i in range(0,len(buffer5),128):
            buffer6=buffer5[i:i+127]
            streamArr=streamArr+Comm.rsaDecrypt(buffer6,privateKey)
        print(streamArr)