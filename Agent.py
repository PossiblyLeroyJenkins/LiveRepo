import time
import json
import requests
import OrderBot
while 1:
	data="SELECT * FROM Queue"
	x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
	y=json.loads(x.content)
	for i in y['data']:
		x = OrderBot.QueryOrder(str(i['orderId']))
		if x['status'] == 'FILLED' and i['alive'] == '1':
			price=format(float(x['price'])*1.005, '.2f')
			quantity=x['origQty']
			OrderBot.PlaceOrder('SELL','LIMIT',price,quantity)
			data = f"UPDATE Queue SET alive = 3 WHERE orderId = \'{x['orderId']}\'"
			x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
			print("placed sell order.")
	print(time.time())
	time.sleep(2)
