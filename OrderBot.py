import hmac
import json
import time
import hashlib
import requests

## THIS COULD AND SHOULD BE A FUNCTION.  BUT IT'S NOT.
## IT ONLY GETS CALLED ONCE, SO I AM CHEATING.
## ASSUME FROM HERE ON OUT API CREDS ARE HARDCODED.
with open('config.ini', 'r') as f:
	configini = json.loads(f.read())
f.close()
api_key=configini['ApiKeys'][0]['api_key']
secret_key=configini['ApiKeys'][0]['secret_key']

##SET THE HEADERS AND BASE URL.
##THESE WILL STAY HARDCODED UNTIL FURTHER NOTICE.
headers = {
	'X-MEXC-APIKEY': api_key,
	'Content-Type': 'application/json'
}
baseurl="https://api.mexc.com"
## MARKET SYMBOL IS SET HERE.  IT IS NEVER CHANGED IN
## THIS SCRIPT, SO I AM HARDCODING IT.  BUT IF YOU NEED
## IT TO CHANGE WITH YOUR SCRIPT, YOU SHOULD START BY
## PUTTING IT IN config.ini AND THEN WRITING A SUB TO
## HANDLE CALLING AND LOADING AND UPDATING.
symbol = 'LTCUSDT'

##################################
def BuyIn(price,bid,baseamount):
	## bid IS A MULTIPLIER. ex: 0.997 IS .3% BELOW MARKET,
	## 1.01 WOULD BE 1 PERCENT ABOVE MARKET. THIS IS A DUMB
	## CALCULATOR.  IT ASKS NO QUESTIONS, MAKE SURE YOU FEED
	## IT THE NUMBERS YOU THINK YOU'RE FEEDING IT.
	price=str(format(float(price)*bid, '.2f'))
	bidamount = str(format(float(baseamount/float(price)), '.8f'))
	return([price,bidamount])
##################################
## TAKES NO PARMS, BUT EASILY COULD.
## RETURNS 1 ON error, ARRAY ON SUCCESS.
def Market():
	# SET ENDPOINT ACCORDING TO MEXC DOCS
	endpoint="/api/v3/depth"
	# SETS LIMIT FOR ORDERS RETURNED
	limit="10"
	# RETURNS EITHER 1 OR CURRENT MARKET PRICES AS DICT
	try:
		x=requests.get(baseurl+endpoint+"?symbol="+symbol+"&limit="+limit)
	except:
		print("Could Not Get Orderbook For Market",symbol)
		return(1)
	return(json.loads(x.content.decode()))

########################################
## TAKES SEVERAL PARAMS. IT WILL FAILL IF IT IS FED
## BAD PARAMS.  I HAVE MADE NO EFFORT TO WRITE ERROR
## CONTROL OR HANDLING.  IF SOMETHING ISN'T WORKING,
## IT IS PROBABLY BREAKING HERE. THERE IS A DIFFERENT
## FUNCTION TO CANCEL ORDERS.
def PlaceOrder(side,order_type,price,quantity):
	## side = 'BUY' OR 'SELL'
	## order_type = 'LIMIT' OR 'MARKET'
	## price = REQUIRED FOR LIMIT ORDERS. BASE CURRENCY.
	## quantity = AMOUNT. TRADE CURRENCY.

	endpoint="/api/v3/order"

	## GENERATES POST BODY.  SEE MEXCI API FOR INFO ON PARAMS.
	timestamp = str(int(time.time() * 1000))  # Current time in milliseconds
	params = f'symbol={symbol}&side={side}&type={order_type}&price={price}&quantity={quantity}&timestamp={timestamp}'
	signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()
	params += f'&signature={signature}'
	response = requests.post(baseurl+endpoint, headers=headers, data=params)

	# Check the response
	if response.status_code == 200:
		xx=json.loads(response.content)
		y=f'INSERT INTO Queue (symbol,orderId,price,origQty,type,side,timestamp) VALUES (\'{symbol}\',\'{xx['orderId']}\',\'{price}\',\'{xx['origQty']}\',\'{xx['type']}\',\'{side}\',\'{str(xx['transactTime'])}\');'
		requests.post('https://www.scrapefarm.click/gridbot/endpoint.php', data=y)
		return(0)
	else:
		print('Error:', response.status_code, response.text)
		exit()
		return(1)
def KillOrder(orderId):
	endpoint="/api/v3/order"
	timestamp = str(int(time.time() * 1000))  # Current time in milliseconds
	params = f'symbol={symbol}&orderId={orderId}&timestamp={timestamp}'
	signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()
	params += f'&signature={signature}'
	response = requests.delete(baseurl+endpoint, headers=headers, data=params)

def QueryOrder(orderId):
	endpoint="/api/v3/order"
	url=baseurl+endpoint
	timestamp = str(int(time.time() * 1000))  # Current time in milliseconds
		# Create the query string
	params = f'symbol={symbol}&orderId={orderId}&timestamp={timestamp}'
		# Create the signature
	signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()
		# Complete the query string with the signature
	params += f'&signature={signature}'
		# Make the GET request
	response = requests.get(url, headers=headers, params=params)
	return(json.loads(response.content))
