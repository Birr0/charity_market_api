from . import router
from fastapi import HTTPException
import schema
import json
from .helpers import EbayBrowse, token



@router.get('/product/{item_id}')
def get_ebay_product(item_id: str):
    #try:
    tk = token(['https://api.ebay.com/oauth/api_scope'])
    product = EbayBrowse(tk).item(item_id)
    charity = EbayBrowse(tk).charity_details(item_id)
    print(product)
    image_list = []
    if 'image' in product:
        image_list.append(product['image']['imageUrl'])
    if 'additionalImages' in product:
        for image in product['additionalImages']:
            image_list.append(image['imageUrl']) 

    return {'product': schema.Product(item_id = product['itemId'],
                        title = product['title'],
                        description =  product['description'] if 'description' in product else '',
                        shortDescription = product['shortDescription'] if 'shortDescription' in product else '',
                        price = product['price']['value'],
                        currency = product['price']['currency'],
                        shipping = json.dumps({'carrier': product['shippingOptions'][0]['shippingServiceCode'], 
                            'type':product['shippingOptions'][0]['type'], 
                            'shippingCost' : product['shippingOptions'][0]['shippingCost'], 
                            'deliveryDate': {'minDate':product['shippingOptions'][0]['minEstimatedDeliveryDate'], 
                            'maxDate':product['shippingOptions'][0]['maxEstimatedDeliveryDate']}, 
                            'moreOptions': 'true' if len(product['shippingOptions']) > 1 else 'false',
                            'additionalCosts': 'true' if 'importCharges' in product['shippingOptions'][0] else 'false',
                         }) if 'shippingOptions' in product else json.dumps({'error':'No shipping options available.'}),
                        itemWebUrl = product['itemWebUrl'],
                        images = image_list,
                        condition = product['condition'] if 'condition' in product else '',
                    )
                    ,
            'charity': schema.Charity(charity_title = charity['charityTitle'],
                        charity_mission = charity['charityMission']
            )
            }
    