from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Json
import json

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
