import json
import time
import requests
import OrderBot

while 1:
	data="SELECT * FROM Queue"
	x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
	y=json.loads(x.content)
	for i in y['data']:
		fuck=(((time.time()*1000)-float(i['timestamp']))/60000)
		if i['alive'] == '1':
			LiveMarket=OrderBot.Market()
			LivePrice=LiveMarket['bids'][0][0]
			Slippage = float(LivePrice)/float(i['price'])
			if fuck > 5 and Slippage > 1.01:
				print("Stale.",time.time())
				print(fuck,Slippage)
				data = f"UPDATE Queue SET alive = 0 WHERE orderId = \'{i['orderId']}\'"
				x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
			else:
				print("Not stale.",time.time())
	print("Sleeping for 10 seconds.",time.time()*1000)
	time.sleep(10)
