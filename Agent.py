import time
import json
import requests
import OrderBot
def Agent():
	data="SELECT * FROM Queue"
	queue=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
	if queue.status_code == 200:
		standingorders=json.loads(queue.content)
		for i in standingorders['data']:
			try:
				x = OrderBot.QueryOrder(str(i['orderId']))
				if x['status'] == 'FILLED' and i['alive'] == '1':
					price=format(float(x['price'])*1.003, '.2f')
					quantity=x['origQty']
					try:
						OrderBot.PlaceOrder('SELL','LIMIT',price,quantity,'Swarm')
						print("Placed Sell Order.",time.time())
						print("Order Added To Swarm.",time.time())
					except:
						print("Fuckery.")
					data = f"UPDATE Queue SET alive = 0 WHERE orderId = \'{x['orderId']}\'"
					try:
						requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
						print("Queue Updated.",time.time())
					except:
						print("Fuckery, but different.")
			except:
				print("SOMETHING WENT WRONG AT:",time.time())
				print(x)
				return(1)
		print("Standing Orders Checked.",time.time())
while 1:
	Agent()
	time.sleep(2)
