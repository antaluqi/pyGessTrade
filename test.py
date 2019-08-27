
import GressTrade
import pprint

api=GressTrade.API()
islog,logMasg=api.login('1021805322','615919')
print(logMasg)


pprint.pprint(api.getTradeInfo())
api.Close()


