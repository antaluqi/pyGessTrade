import hashlib


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