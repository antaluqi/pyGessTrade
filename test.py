
import GressTrade

api=GressTrade.API()
islog,logMasg=api.login('1021805322','615919')
api.getCustInfo()
print(api.custInfo.ToString())

