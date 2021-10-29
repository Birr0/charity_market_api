from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import Optional

class Charity(BaseModel):
    charity_title: str
    charity_mission: str
    logo: Optional[HttpUrl]

class CharityList(str, Enum):
    british_heart_foundation: 17719
    RNLI: 16159
    svp_england_and_wales: 97905
    british_red_cross: 19790