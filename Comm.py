import hashlib
import OpenSSL
import rsa
from dateutil import parser

'''
字符串填充
str：原字符串
fillStr：填充字符串
maxLen：填充后长度
dir：填充方向
'''
def Fill(str,fillStr,maxLen,dir):
    if dir=='L':
        return str.rjust(maxLen,fillStr)
    elif dir=='R':
        return str.ljust(maxLen,fillStr)
    else:
        raise Exception("dir必须为 R 或 L")


'''
MD5
'''
def MD5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()


'''
获取.crt 文件中的 publickey
返回字符串形式
学习网址：https://www.cnblogs.com/qq874455953/p/10264428.html
'''
def getCrtFilePublickey(file_path):
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(file_path).read())
    pubkey=OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
    return pubkey

'''
获取.pfx文件中的privatekey
返回二进制形式
学习网址：https://blog.csdn.net/qq_24833677/article/details/88869404
'''
def getPfxFilePrivatekey(file_path,pw):
    cert=OpenSSL.crypto.load_pkcs12(open(file_path, 'rb').read(),pw)
    return OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, cert.get_privatekey())


'''
rsa加密
学习网址：https://blog.csdn.net/huangqingsong_5678/article/details/79358806
'''
def rsaEncrypt(bitInfo,pubKey):
    publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(pubKey)
    return rsa.encrypt(bitInfo, publicKey)


'''
rsa解密
学习网址：https://blog.csdn.net/huangqingsong_5678/article/details/79358806
'''
def rsaDecrypt(bitInfo,pvtKey):
    privateKey=rsa.PrivateKey.load_pkcs1(pvtKey,'DER')
    return rsa.decrypt(bitInfo, privateKey)