
import GressTrade
import pprint
import os
api=GressTrade.API()
islog,logMasg=api.login('1021805322','615919')
print(logMasg)

api.getQuote()
pprint.pprint(api.quote.mautd.toDict())
api.Close()



