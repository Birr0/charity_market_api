from typing import Optional
from . import router
from .helpers import EbayBrowse, token
from schema import Filter
from statistics import mode

@router.post('/search/{query}')
def keyword_search(query: str, limit: int, filter: Filter, page: Optional[int] = 1 ):
    ebay_filter = 'charityOnly:true'
    if filter:
        ebay_price_range = f'[{filter.min_price if filter.min_price else 0}..{filter.max_price if filter.max_price else 10000}]'
        
        ebay_filter += f",price:{ebay_price_range},priceCurrency:{filter.currency.value if filter.currency else 'GBP'}"
    
        if filter.conditions:
            condition_list = ''
            for i in range(len(filter.conditions)):
                if i == (len(filter.conditions) - 1):
                    condition_list += filter.conditions[i].value
                else:
                    condition_list += f'{filter.conditions[i].value}|'
    
            ebay_filter += (",conditionIds:{" + condition_list + "}")
        
        if filter.returns_accepted:
            ebay_filter += ",returnsAccepted:true"
        
        if filter.search_in_description:
            ebay_filter += ",searchInDescription:true"
        
        if filter.seller_type:
            if filter.seller_type == 'BUSINESS':
                ebay_filter += ",sellerAccountTypes:{BUSINESS}"
            
            if filter.seller_type == 'INDIVIDUAL':
                ebay_filter += ",sellerAccountTypes:{INDIVIDUAL}"
            
            else:
                pass
    
    return  EbayBrowse(token(['https://api.ebay.com/oauth/api_scope'])).item_summary({'q' : query, 'filter': ebay_filter, 'limit': limit, 'offset': (page - 1) * limit})


@router.post('/recommended-products')
def get_recommended_products(userData: dict):
    
    categories = []
    if 'interactions' in userData:
        for item in userData['interactions']['productsViewed']:
            if 'categories' in item:
                for entry in item['categories']:
                    categories.append(int(entry['categoryId']))
        #for item in userData['interactions']['categoriesViewed']:
        for item in userData['interactions']['categoriesViewed']:
            categories.append(int(item['ebid']))
        recommended_category = mode(categories)
    else:
        recommended_category = '20091'
    
    
    return {'recommended_category': recommended_category, 'recommended_search_list': []}
