from pydantic import BaseModel, Json
from typing import Optional

class Category(BaseModel):
    name: str
    ebid: str
    subcategories: Optional[dict] = {}