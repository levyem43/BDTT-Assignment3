from requests import Session
import secrets

from db_config import get_redis_connection
import json

from pprint import pprint as pp

class CMC:
    
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token,}
        self.session = Session()
        self.session.headers.update(self.headers)
        
    def get50Coins(self):
        url = self.apiurl + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data'][0:50]
        return data
    
    def getCurrencyQuote(self, symbol, convert='USD'):
        url = self.apiurl + '/v2/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol,'convert':convert}
        r = self.session.get(url, params=parameters)
        data = r.json()['data']
        return data
    
    def getCurrencyPriceConverted(self,symbol,convert='USD'):
        return self.getCurrencyQuote(symbol)[symbol][0]['quote'][convert]['price']
    
cmc = CMC(secrets.API_KEY)

# currency = cmc.get50Coins()

# coin_types = []
# for i in range(len(currency)):
#     coin_types.append(currency[i]['symbol'])
# print(coin_types)

BTCtoUSD = cmc.getCurrencyPriceConverted('BTC')

print(BTCtoUSD)

# r = get_redis_connection()

# jane = {'name': "Jane",'Age': 33,'Location': "Chawton"}

# r.set('my_key', json.dumps(cmc.getPrice('BTC')))

# pp(json.loads(r.get('my_key')))
