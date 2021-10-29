from . import router
import schema
import requests
import urllib
import json

'''
class Product(BaseModel):
    
    item_id: str
    title: str
    short_description: Optional[str]
    description : Optional[str]
    price: str
    currency: str
    itemWebUrl: Optional[HttpUrl] # add tracking link
    images: List[HttpUrl]
    condition: Optional[str] # add schema
    shipping: Optional[Json]
    attributes: Optional[Json]

'''

@router.get('/oxfam/search/{query}')
def oxfam_search(query: str, limit: int):
    scraped_products = []
    q = urllib.parse.quote(query)
    x = requests.get(f'https://onlineshop.oxfam.org.uk/ccstoreui/v1/search?N=&Nrpp={limit}&No=0&Nr=product.active%3A1&Ntt={query}')
    response = x.json()
    products = response['resultsList']

    for product in products['records']:
        attributes = product['records'][0]['attributes']
        
        
        sanitized_product = schema.Product(
                item_id = attributes['sku.listingId'][0],
                title = attributes['sku.displayName'][0],
                description = attributes['product.longDescription'][0],
                price = attributes['sku.listPrice'][0],
                currency = 'GBP',
                itemWebUrl = 'https://onlineshop.oxfam.org.uk'.format(attributes['product.route'][0]),
                images = ['https://onlineshop.oxfam.org.uk{}'.format(attributes['product.primaryFullImageURL'][0])],
                condition =  attributes['product.ox_condition'][0] if 'product.ox_condition' in attributes else 'Unknown',
                shipping = json.dumps({'shippingCost': attributes['product.shippingSurcharge'][0] if 'product.shippingSurchage' in attributes else ''}),
                attributes = json.dumps(attributes)
                )

        scraped_products.append(sanitized_product)

    print('Number of products {}'.format(products['totalNumRecs']))
    return {'products' : scraped_products,
         'charity': schema.Charity(
             charity_title = 'Oxfam UK', 
             charity_mission = 'We function in exactly the same way as any major online retailer, \
              but there is one thing that sets us apart. Every penny rasied by your purchases will \
              help ordinary families to work their way out of poverty.')}

'''
Get item id for search terms ...
(max number returned 250 ...)
https://onlineshop.oxfam.org.uk/ccstoreui/v1/search?N=&Nrpp=250&No=0&Nr=product.active%3A1&Ntt=mathematics

resultsList.records = [n].attributes ... (repositoryId)

'''

'''
Get items from list of ids ...

'https://onlineshop.oxfam.org.uk/ccstoreui/v1/products?storePriceListGroupId=ukPriceGroup&productIds=HD_101478812%2CHD_101520736%2CHD_101644946%2CHD_101583086%2CHD_101467346%2CHD_300200627%2CHD_101611087%2CHD_101440446%2CHD_101541037%2CHD_200100626%2CHD_101794020%2CHD_200351174'
'''

