from pydantic import BaseModel, Json
from typing import Optional, List
from schema.charity import CharityList

from schema.product.conditions import EbayCondition
from . import Currency
from .product import conditions

class Filter(BaseModel):
    min_price: Optional[int]
    max_price: Optional[int]
    currency: Optional[Currency]
    search_in_description: Optional[bool] #returns items with keyword in title/description for ebay
    returns_accepted: Optional[bool]
    #specified_sellers: Optional[List[CharityList]] # List of eBay ids
    specified_sellers: Optional[List[CharityList]]
    seller_type: Optional[str] # might be useful for filtering out charities ...
    conditions: Optional[List[conditions.EbayCondition]]
