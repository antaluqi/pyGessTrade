
import GressTrade
api=GressTrade.API()
islog,logMasg=api.login('1021805322','615919')
print(logMasg)
#api.getTradeInfo()
api.getQuote()
print(api.quote.mautd.ToString())
api.Close()


