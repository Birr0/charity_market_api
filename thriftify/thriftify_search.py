import requests
from bs4 import BeautifulSoup
import urllib.parse
import aiohttp
import asyncio
import time
#from .schema import Product

async def get_product(session, url, products):
    async with session.get(url) as resp:
        data = await resp.content
        return data
        #soup = BeautifulSoup(data.content, 'html.parser')
        #html_products = soup.find_all("li", {"class": "item product product-item"})
        #products.append(html_products)
        #return products
        '''
        for product in html_products:
            products.append(Product(
                item_id = str,
                title = str,
                short_description =  Optional[str],
                description = Optional[str]
                price = str,
                currency = str,
                itemWebUrl = Optional[HttpUrl], # add tracking link
                images: List[HttpUrl]
                condition: Optional[str] # add schema
                shipping: Optional[Json]
            ))
        '''
        #return products

def get_first_request(q: str):
    q = urllib.parse.quote(q)
    data = requests.get(f'https://www.thriftify.co.uk/catalogsearch/result/?q={q}')
    soup = BeautifulSoup(data, 'html.parser')
    print(soup)
    number_of_pages = round(int(soup.find_all('span', {'class':'toolbar-number'})[-1].text)/int(soup.find_all('span', {'class':'toolbar-number'})[-2].text))


async def thriftify_search(q: str):
    start_time = time.time()
    
    q = urllib.parse.quote(q)
    url = 'https://www.thriftify.co.uk/catalogsearch/result/?q={q}'

    #async with session.get(url, ssl=False) as response:
    #    obj = await response.read()
    #    all_offers[url] = obj

    async with aiohttp.ClientSession() as session:
        products = []
        async with session.get(url, ssl=False) as response:
            print(response)

            raw_html = await response.text()
            soup = BeautifulSoup(raw_html, 'html.parser')
            number_of_pages = round(int(soup.find_all('span', {'class':'toolbar-number'})[-1].text)/int(soup.find_all('span', {'class':'toolbar-number'})[-2].text))

            #print(soup)
        tasks = []
        for number in range(2, number_of_pages):
            page_url = url + f'&p={number}'
            tasks.append(asyncio.ensure_future(get_product(session, page_url, products)))
#
            #response = await asyncio.gather(*tasks)
            #for product in products:
            #    print(product)
    print(time.time() - start_time)
    return #data

asyncio.run(thriftify_search('Mens shoes'))
#loop = asyncio.get_event_loop()
#loop.run_until_complete(thriftify_search('Mens shoes'))

'''
<div class="product details product-item-details">
<div class="product name product-item-name">
    <a class="product-item-link" href="https://www.thriftify.co.uk/catalog/product/view/id/57508/s/pregnancy-for-men-the-whole-nine-months-paperback-32575-5f6deeb7a4160/category/2/">
                                      Pregnancy for Men: The whole nine months (PAPERBACK)                                        </a>
    </div>
    <div class="price-box price-final_price" data-price-box="product-id-57508" data-product-id="57508" data-role="priceBox">
    <span class="price-container price-final_price tax weee">
    <span class="price-wrapper" data-price-amount="7.25" data-price-type="finalPrice" id="product-price-57508"><span class="price">£7.25</span></span>
    </span>
    </div>
    </div>
    </div>
    </div>
    </li>
    <li class="item product product-item">
    <div class="item-inner">
    <div class="product-item-info" data-container="product-grid">
    <div class="product-item-image">
    <a class="product photo product-item-photo" href="https://www.thriftify.co.uk/dunnes-stores-grey-mens-trousers-size-xxl.html" tabindex="-1">
    <span class="product-image-wrapper">
    <img alt="Dunnes Stores Grey Mens Trousers - Size XXL" class="product-image-photo default_image" data-original="https://www.thriftify.co.uk/media/catalog/product/cache/188783fe596f666966ed3f1d175588ba/1/7/17_18_10.jpg" src="https://www.thriftify.co.uk/static/version1634273972/frontend/RLTThriftify/RLTConsumer/en_GB/Magefan_LazyLoad/images/pixel.jpg"/>
    <noscript>
    <img alt="Dunnes Stores Grey Mens Trousers - Size XXL" class="product-image-photo default_image" src="https://www.thriftify.co.uk/media/catalog/product/cache/188783fe596f666966ed3f1d175588ba/1/7/17_18_10.jpg"/>
    </noscript>
    </span>
    </a>
    <div class="button-top">
    <a class="action tocart primary" data-post='{"action":"https:\/\/www.thriftify.co.uk\/checkout\/cart\/add\/uenc\/aHR0cHM6Ly93d3cudGhyaWZ0aWZ5LmNvLnVrL2NhdGFsb2dzZWFyY2gvcmVzdWx0Lz9xPU1lbnMlMjBzaG9lcw%2C%2C\/product\/69099\/","data":{"product":"69099","uenc":"aHR0cHM6Ly93d3cudGhyaWZ0aWZ5LmNvLnVrL2NhdGFsb2dzZWFyY2gvcmVzdWx0Lz9xPU1lbnMlMjBzaG9lcw,,"}}' title="Add to Cart">
    <span>Add to Cart</span>
    </a>
    <a class="action tocompare" data-post='{"action":"https:\/\/www.thriftify.co.uk\/catalog\/product_compare\/add\/","data":{"product":"69099","uenc":"aHR0cHM6Ly93d3cudGhyaWZ0aWZ5LmNvLnVrL2NhdGFsb2dzZWFyY2gvcmVzdWx0Lz9xPU1lbnMlMjBzaG9lcw,,"}}' href="#" title="Add to Compare">
    <span>Add to Compare</span>
    </a>
</div>
'''