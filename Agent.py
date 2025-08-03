import time
import json
import requests
import OrderBot
def Agent():
	data="SELECT * FROM Queue"
	x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
	y=json.loads(x.content)
	for i in y['data']:
		try:
			x = OrderBot.QueryOrder(str(i['orderId']))
			if x['status'] == 'FILLED' and i['alive'] == '1':
				price=format(float(x['price'])*1.003, '.2f')
				quantity=x['origQty']
				OrderBot.PlaceOrder('SELL','LIMIT',price,quantity,'Swarm')
				data = f"UPDATE Queue SET alive = 0 WHERE orderId = \'{x['orderId']}\'"
				x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
				print("XXplaced sell orderXX.")
		except:
			print("SOMETHING WENT WRONG AT:",time.time())
			if x:
				print(x,x.contents)
			return(1)
	print("Standing Orders Checked.",time.time())
while 1:
	Agent()
	time.sleep(2)
