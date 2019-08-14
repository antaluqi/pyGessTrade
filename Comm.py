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
打印.crt 证书文件的信息
'''
def crtFileinfo(file_path):
    # "./cert/server.crt"
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(file_path).read())
    certIssue = cert.get_issuer()
    print("证书版本:            ", cert.get_version() + 1)
    print("证书序列号:          ", hex(cert.get_serial_number()))
    print("证书中使用的签名算法: ", cert.get_signature_algorithm().decode("UTF-8"))
    print("颁发者:              ", certIssue.commonName)
    datetime_struct = parser.parse(cert.get_notBefore().decode("UTF-8"))
    print("有效期从:             ", datetime_struct.strftime('%Y-%m-%d %H:%M:%S'))
    datetime_struct = parser.parse(cert.get_notAfter().decode("UTF-8"))
    print("到:                   ", datetime_struct.strftime('%Y-%m-%d %H:%M:%S'))
    print("证书是否已经过期:      ", cert.has_expired())
    print("公钥长度", cert.get_pubkey().bits())
    print("公钥:\n", OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8"))
    print("主体信息:")
    print("CN : 通用名称  OU : 机构单元名称")
    print("O  : 机构名    L  : 地理位置")
    print("S  : 州/省名   C  : 国名")
    for item in certIssue.get_components():
        print(item[0].decode("utf-8"), "  ——  ", item[1].decode("utf-8"))
    print(cert.get_extension_count())


'''
获取.crt 文件中的 publickey
'''
def getCrtFilePublickey(file_path):
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(file_path).read())
    pubkey=OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
    return pubkey


def getPfxFilePrivatekey(file_path,pw):
    cert=OpenSSL.crypto.load_pkcs12(open(file_path, 'rb').read(),pw)
    return OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, cert.get_privatekey())


'''
rsa加密
'''
def rsaEncrypt(bitInfo,pubKey):
    publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(pubKey)
    return rsa.encrypt(bitInfo, publicKey)


'''
rsa解密
'''
def rsaDecrypt(bitInfo,pvtKey):

    privateKey=rsa.PrivateKey.load_pkcs1_openssl_pem(pvtKey)
    return rsa.encrypt(bitInfo, privateKey)