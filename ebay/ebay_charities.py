from schema import country_codes
from . import router
import requests
from typing import Optional, List
from schema import CountryCode
from .helpers import token
import json

class EbayCharities():
    def __init__(self, APP_AUTH_TOKEN ,country_code):
        self.headers = {'Accept-Encoding':'application/gzip','Content-Language':f'en-{country_code}','Content-Type':'application/json','X-EBAY-C-MARKETPLACE-ID':f'EBAY_{country_code}','Authorization':APP_AUTH_TOKEN}

    def get_charities(self, q):
        return requests.get(f'https://api.ebay.com/commerce/charity/v1/charity_org?q={q}', headers = self.headers).json()

@router.get('/charities')
def get_charities(country_code: CountryCode, q: str, limit: int, offset: int):
    tk = token(['https://api.ebay.com/oauth/api_scope'])
    return EbayCharities(APP_AUTH_TOKEN = tk, country_code = country_code.value).get_charities(q = q)


@router.get('/charity/{charity_id}/products')
def get_charity(charity_id: str, page: Optional[int]):
    tk = token(['https://api.ebay.com/oauth/api_scope'])
    headers = {'Accept-Encoding':'application/gzip','Content-Language':'en-GB','Content-Type':'application/json','X-EBAY-C-MARKETPLACE-ID':f'EBAY_GB','Authorization':tk}
    return requests.get(f'https://api.ebay.com/buy/browse/v1/item_summary/search?charity_ids={charity_id}&fieldgroups=FULL&filter=charityOnly:true,sellerAccountTypes:{{BUSINESS}}&limit=39&offset={((page - 1) * 39) if page else 0}', headers = headers).json()
    
    '''
    charities = []
    #for i in range(0, 1000, 1):
       # query += (str(i) + ',')
    
    with open('active_charities.json', 'r') as f:
        x = json.load(f)
    print(len(x))

    
    
    for item in x:
        #charities.append(item)
        if 'registrationId' in item:
            r = requests.get('https://api.ebay.com/buy/browse/v1/item_summary/search?charity_ids={}'.format(item['registrationId']), headers=headers).json()
            if 'total' in r:
                if r['total'] > 0:
                    charities.append(item)
    
    with open('active_charities.json', 'w') as file:
        json.dump(charities, file, indent=4)
    #r = requests.get(f'https://api.ebay.com/buy/browse/v1/item_summary/search?charity_ids={charity_id}', headers=headers).json()
    '''
    #r = requests.get(f'https://api.ebay.com/buy/browse/v1/item_summary/search?charity_ids={charity_id}', headers=headers).json()
    
    #return r
    #r = requests.get(f'https://api.ebay.com/commerce/charity/v1/charity_org?q=a&limit=100', headers = headers).json()
    '''
    charities += r['charityOrgs']
    iterations = round(r['total'] / 100)
    
    for i in range(iterations):
        try:
            offset = 100 * (i + 1)
            x =  requests.get(f'https://api.ebay.com/commerce/charity/v1/charity_org?q=a&limit=&offset={offset}', headers = headers).json()
            
            charities += x['charityOrgs']
            
        except:
            pass
    with open('active_charities.json', 'w') as f:
        json.dump(charities, f, indent=4)
    return charities
    '''