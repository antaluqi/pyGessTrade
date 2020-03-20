
import GressTrade
import pprint
import time
api=GressTrade.API()
islog,logMasg=api.login('1021805322','615919')
print(logMasg)

for i in range(100):
    api.getQuote()
    print(api.quote.mautd.last)
api.Close()



