import time
import json
import requests
import OrderBot
while 1:
	data="SELECT * FROM Queue"
	x=requests.post("https://www.scrapefarm.click/gridbot/endpoint.php", data=data)
	y=json.loads(x.content)
	break
print(y)
