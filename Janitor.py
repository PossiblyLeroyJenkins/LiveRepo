import json
import time
import requests
import OrderBot
while 1:
	data="SELECT * FROM Queue"
	x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
	y=json.loads(x.content)
	for i in y['data']:
		if i['alive'] == '0':
			print("that bot is dead.\n",i)
			OrderBot.KillOrder(str(i['orderId']))
			data="DELETE FROM Queue WHERE alive = '0';"
			requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
		if i['alive'] == '3':
			print("Sold.  Doesn't need to be here.\n",i)
			OrderBot.KillOrder(str(i['orderId']))
			data="DELETE FROM Queue WHERE alive = '3';"
			requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)

	print("Sleeping for ten seconds.",time.time())
	time.sleep(10)
