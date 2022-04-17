import requests
import base64
import os
from bs4 import BeautifulSoup

#---Generate OAuth tokens---#

class EbayOauth():
    def __init__(self, client_credentials):
        self.client_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')
        self.url = 'https://api.ebay.com/identity/v1/oauth2/token'
    def client_credentials_token(self, scope):
        headers = {'Content-Type':'application/x-www-form-urlencoded', 'Authorization':'Basic {}'.format(self.client_credentials)}
        payload = {'grant_type':'client_credentials', 'scope': scope}
        response = requests.post(self.url, headers = headers , params = payload).json()
        try:
            return response['access_token']
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
        
        
def token(scope):
    token = EbayOauth(os.getenv('CLIENT_CREDENTIALS')).client_credentials_token(scope)
    return f'Bearer {token}'

#---Buy APIS ---#

class EbayBrowse():
    def __init__(self, APP_AUTH_TOKEN):
        self.headers = {'Accept-Encoding':'application/gzip','Content-Language':'en-GB','Content-Type':'application/json','X-EBAY-C-MARKETPLACE-ID':'EBAY-GB','Authorization':APP_AUTH_TOKEN}

    def item_summary(self, payload):
        try:
            r = requests.get('https://api.ebay.com/buy/browse/v1/item_summary/search', headers=self.headers, params = payload)
            return r.json()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            raise SystemExit(err)
        return
    
    def item(self, item_id):
        try:
            r = requests.get(f'https://api.ebay.com/buy/browse/v1/item/{item_id}', headers=self.headers)
            return r.json()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Something Else",err)
            raise SystemExit(err)
        return

    def charity_details(self, item_id):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        item_id = (item_id.split('v1|'))[1].split('|0')[0]
        r = requests.get(f'https://www.ebay.co.uk/itm/{item_id}')
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            return {'charityTitle':soup.find('span', attrs ={'class':'charityTitle'}).text.strip(),'charityMission':soup.find('div', attrs ={'class':'charityMission'}).text.strip()}
        except:
            return {'charityTitle': 'Not available', 'charityMission': 'Not available'}
            

#---Commerce APIS ---#

class EbayCommerce():
    def __init__(self):
        self.headers = {'Accept-Encoding':'application/gzip','Content-Language':'en-GB','Content-Type':'application/json','X-EBAY-C-MARKETPLACE-ID':'EBAY-GB','Authorization':APP_AUTH_TOKEN}
    
    def catalog(self, payload): ## Not Working! insufficient permissions. Need to generate OAuth token before...
        r = requests.get('https://api.ebay.com/commerce/catalog/v1_beta/product_summary/search?', headers=self.headers, params=payload)

#--- Taxonomy ---#

class Taxonomy(): #1059
    def __init__(self,APP_AUTH_TOKEN):
         self.headers = {'Accept-Encoding':'application/gzip','Content-Language':'en-GB','Content-Type':'application/json','X-EBAY-C-MARKETPLACE-ID':'EBAY-GB','Authorization':APP_AUTH_TOKEN}
    def get_default_category_tree_id(self):
        payload = {'marketplace_id':'EBAY_GB'}
        r = requests.get('https://api.ebay.com/commerce/taxonomy/v1/get_default_category_tree_id?', headers=self.headers, params=payload)
        return r.json()
    def get_category_subtree(self, category_id):
        payload = {'category_id': category_id}
        r = requests.get(f'https://api.ebay.com/commerce/taxonomy/v1/category_tree/3/get_category_subtree?', headers=self.headers, params=payload)
        return r.json()
    def get_category_tree(self, category_id):
        payload = {'category_id': category_id}
        r = requests.get(f'https://api.ebay.com/commerce/taxonomy/v1/category_tree/{category_id}', headers=self.headers, params = payload)
        return r.json()