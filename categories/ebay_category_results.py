from ebay.helpers import EbayBrowse, token
from . import router
import time
from schema import Category
from typing import Optional, List

mens_categories = {'Belts' :'2993','Wallets':'2996','Ties, Bow Ties & Cravats': '15662', 
    'Bags': '52357','Umbrellas':'90634','Sunglasses & Sunglasses Accessories':'179239',
    'Boots':'11498','Sandals & Beach Shoes':'11504','Trainers':'15709','Casual Shoes':'24087',
    'Formal Shoes':'53120','Suits & Tailoring':'3001','Jeans':'11483','Jumpers & Cardigans':'11484',
    'Coats, Jackets & Waistcoats':'57988','Trousers':'57989','Activewear':'185099','T-Shirts':'15687',
    'Casual Shirts & Tops':'57990','Formal Shirts':'57991','Polos':'185101','Hats':'52365'}

womens_categories = {'Jumpsuits & Playsuits':'3009','Jeans':'11554','Shorts':'11555',
        'Tops & Shirts':'53159','Dresses':'63861','Coats, Jackets & Waistcoats':'63862','Skirts':'63864',
        'Suits & Suit Separates':'63865','Jumpers & Cardigans':'63866','Hoodies & Sweatshirts':'155226',
        "Women's Bags & Handbags":'169291','Belts':'3003','Organisers & Diaries':'15735', 'Accessory Sets':'15738', 
        'Hair Accessories': '45220','Hats':'45230','Scarves & Shawls':'45238','Purses & Wallets':'45258','Umbrellas':'105569','Sunglasses & Sunglasses Accessories':'179247',
        'Boots':'53557','Flats':'45333','Comfort Shoes':'53548','Heels':'55793','Sandals':'62107','Trainers':'95672'}

dvds = '617'

cd = '176984'

ebay_books = '261186'
oxfam_books = '1129593664'


ebay_fiction_genres = {'Action & Adventure','Adult & Erotic','Ancient Literature',
        'Classics','Comics','Crime & Thriller','Drama','Fairy Tale',
        'Fantasy','Folklore & Mythology','Historical','Horror',
        'Humour','LGBT','Modern & Contemporary','Pulp Fiction',
        'Historical','Religious & Spiritual','Romance','Science Fiction',
        'Romance','Urban Fiction','War & Combat','Western',"Women's Fiction",'Not specified'}

ebay_non_fiction_genres = {'Animals & Pets','Art & Culture','Biographies & True Stories',
    'Environment, Nature & Earth', 'Family, Parenting & Relations','Food & Drink',
    'History & Military', 'Law', 'Leisure, Hobbies & Lifestyle', 'Mathematics & Sciences',
    'Philosophy', 'Religion & Beliefs', 'Sports', 'Transport', 'Travel', 'Not specified'}

categories = [{'name': 'Books','title':'Books' ,'ebid': '261186', 'categoryImage': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=873&q=80'},{'name': 'DVDs', 'title':'DVDs','ebid': '617'},{'name': 'CDs', 'title':'CDs','ebid': '176984'},  
{'name': 'womens', 'title':"Women's",'ebid': '260010', 'subcategories': 
{'jumpsuits-playsuits': {'name': 'Jumpsuits & Playsuits', 'ebid': '3009'}, 
'jeans': {'name': 'Jeans', 'ebid': '11554'}, 
'shorts': {'name': 'Shorts', 'ebid': '11555'}, 
'tops-shirts': {'name': 'Tops & Shirts', 'ebid': '53159'}, 
'dresses': {'name': 'Dresses', 'ebid': '63861'}, 'coats-jackets-waistcoats': {'name': 'Coats, Jackets & Waistcoats', 'ebid': '63862'},
'skirts': {'name': 'Skirts', 'ebid': '63864'}, 'suits': {'name': 'Suits & Suit Separates', 'ebid': '63865'}, 
'jumpers-cardigans': {'name': 'Jumpers & Cardigans', 'ebid': '63866'}, 'hoodies-sweatshirts': {'name': 'Hoodies & Sweatshirts', 'ebid': '155226'},
"bags-handbags": {'name': "Women's Bags & Handbags", 'ebid': '169291'}, 'belts': {'name': 'Belts', 'ebid': '3003'}, 
'organisers-diaries': {'name': 'Organisers & Diaries', 'ebid': '15735'}, 'accessory-sets': {'name': 'Accessory Sets', 'ebid': '15738'},
'hair-accessories': {'name': 'Hair Accessories', 'ebid': '45220'}, 'hats': {'name': 'Hats', 'ebid': '45230'}, 
'scarves-shawls': {'name': 'Scarves & Shawls', 'ebid': '45238'}, 'purses-wallets': {'name': 'Purses & Wallets', 'ebid': '45258'}, 
'umbrellas': {'name': 'Umbrellas', 'ebid': '105569'}, 'sunglasses': {'name': 'Sunglasses & Sunglasses Accessories',
'ebid': '179247'}, 'boots': {'name': 'Boots', 'ebid': '53557'}, 'flats': {'name': 'Flats', 'ebid': '45333'}, 
'comfort-shoes': {'name': 'Comfort Shoes', 'ebid': '53548'}, 'heels': {'name': 'Heels', 'ebid': '55793'},
'sandals': {'name': 'Sandals', 'ebid': '62107'}, 'trainers': {'name': 'Trainers', 'ebid': '95672'}}},
{'name': "mens", 'title': "Men's",'ebid': '260012', 'subcategories': 
{'belts' : {'name': "Belts", 'ebid': '2993'},'wallets':{'name': "Wallets",'ebid' : '2996' },
'ties': {'name': 'Ties, Bow Ties & Cravats','ebid':'15662'}, 'bags':{'name': 'Bags','ebid':'52357'},'umbrellas':{'name': 'Umbrellas','ebid':'90634'},
'sunglasses':{'name' : 'Sunglasses & Sunglasses Accessories' ,'ebid':'179239'},'boots':{'name':'Boots','ebid': '11498'},
'sandals':{'name':'Sandals & Beach Shoes','ebid': '11504'}, 'trainers':{'name':'Trainers','ebid':'15709'}, 
'casual-shoes':{'name': 'Casual Shoes','ebid':'24087'} , 'formal-shoes':{'name': 'Formal shoes','ebid':'53120'},
'suits':{'name':'Suits & Tailoring', 'ebid':'3001'},'jeans':{'name': 'Jeans','ebid':'11483'}, 'jumpers':{'name':'Jumpers & Cardigans', 'ebid':'11484'},
'coats':{'name':'Coats, Jackets & Waistcoats', 'ebid':'57988'},'trousers':{ 'name': 'Trousers','ebid':'57989'},'activewear':{'name': 'Activewear','ebid':'185099'},
't-shirts':{'name':'T-Shirts', 'ebid':'15687'}, 'casual-shirts':{'name': 'Casual Shirts & Tops', 'ebid':'57990'},'formal-shirts':{'name':'Formal Shirts','ebid':'57991'},
'polos':{'name':'Polos', 'ebid':'185101'} ,'hats':{'name':'Hats', 'ebid':'52365'}}}, {'name': 'art', 'title': 'Art', 'ebid': '550'}, {'name': 'collectables', 'title':'Collectables','ebid': '1', 'categoryImage':'https://images.unsplash.com/photo-1591287968288-394880ef65a0?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1170&q=80', 
'subcategories': {'coins-banknotes' : {}}},{'name': 'furniture', 'title':'Furniture','ebid': '3197', 'categoryImage':'https://images.unsplash.com/photo-1591287968288-394880ef65a0?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1170&q=80', 
'subcategories': {'sofas-armchairs' : {'name': "Sofa and Armchairs", 'ebid': '38208'}}}]

@router.post('/categories/{category_name}')
def get_ebay_category_results(category_name: str, limit: int, page: int, category: Category,  subcategory_name: Optional[str] = '', aspect_filter: Optional[str] = '', filter: Optional[str] = 'charityOnly:true,conditions:{USED},sellerAccountTypes:{BUSINESS}'): # seems to filter out for actual charity retailers ...
    print(category)
    print('HK')
    print(aspect_filter)
    print(filter)
    
    if category.subcategories:
        return EbayBrowse(token(scope = ['https://api.ebay.com/oauth/api_scope'])).item_summary({'category_ids': category.subcategories[subcategory_name]['ebid'] if subcategory_name in category.subcategories else category.ebid ,'filter':filter,'aspect_filter': aspect_filter if aspect_filter else 'categoryId:{}'.format(category.subcategories[subcategory_name]['ebid']),'fieldgroups':'FULL','limit': limit, 'offset': (page - 1) * limit})
    else:
        data = EbayBrowse(token(scope = ['https://api.ebay.com/oauth/api_scope'])).item_summary({'category_ids': category.ebid ,'filter':filter if filter else 'charityOnly:true,conditions:{USED},sellerAccountTypes:{BUSINESS}','aspect_filter': aspect_filter if aspect_filter else 'categoryId:{}'.format(category.ebid),'fieldgroups':'FULL','limit': limit, 'offset': (page - 1) * limit}) 
        return data

@router.get('/categories/{category_id}')
def get_ebay_category_results(category_id: str, limit: int, page: int,  subcategory_name: Optional[str] = '', aspect_filter: Optional[str] = '', filter: Optional[str] = 'charityOnly:true'):
    return EbayBrowse(token(scope = ['https://api.ebay.com/oauth/api_scope'])).item_summary({'category_ids': category_id, 'filter':'charityOnly:true,conditions:{USED},sellerAccountTypes:{BUSINESS}','aspect_filter':'categoryId:{},conditionDistributions:'.format(category_id) + '{USED}','limit': limit, 'offset': (page - 1) * limit})
    
#https://onlineshop.oxfam.org.uk/ccstoreui/v1/search?N={}&Nrpp=30&No=0&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=product.creationDate%7C1
#https://onlineshop.oxfam.org.uk/ccstoreui/v1/pages/category/{category_name}?dataOnly=false&cacheableDataOnly=true&productTypesRequired=false

'''
oxfam_non_fiction_genres = {'Antique&Collectible': 3131036302, 'Art&Photography':3961531481, 'Biographies': 1129593664, 'Business, Finance and Law': 1129593664, 'Comics and graphic novels': 1129593664}
NON-FICTION
Antiquarian, Rare and Collectable
Art and Photography
Biographies
Business, Finance and Law
Childrens
Comics and Graphic Novels
Crime
Fiction
Food and Drink
Games and Gift
History
Home, Garden and Crafts
LGBTQ+
Lifestyle
Music
Nature and Pets
Poetry, Drama and Criticism
Reference & Languages
Religion and Spirituality
Science Fiction, Fantasy and Horror
Science and Medicine
Society, Politics and Philosophy
Sports
Stage and Screen
Stationery and Journals
Transport
Travel and Holiday 
'''

'''
Oxfam fiction
Classics
Female writers & fiction
Fiction in a Foreign Language
Historical, Westerns, & War
Literary fiction
Other
Political
Romance
Short Stories 

'''