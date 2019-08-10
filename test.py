import rsa

with open('./cert/server.crt' ,'r') as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    print(pubkey)