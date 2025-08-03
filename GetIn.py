import OrderBot
import requests
#import hmac
import json
MarketPrices=OrderBot.Market()
## THIS IS NOT A MAGIC NUMBER, IT IS DOCUMENTED IN THE LIB.
bid=OrderBot.BuyIn(MarketPrices['bids'][0][0], 0.5, 1.01)
## THIS IS NOT A MAGIC NUMBER, IT IS DOCUMENTED IN THE LIB.
print(bid)
#OrderBot.PlaceOrder('BUY', 'LIMIT', bid[0], bid[1])
OrderBot.PlaceOrder('BUY', 'LIMIT', .5, 2)
