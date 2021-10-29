from enum import Enum

class EbayCondition(str, Enum):
    new = 1000
    new_other = 1500
    new_with_defects = 1750
    certified_refurbished = 2000
    refurbished_excellent = 2010
    refurbished_very_good = 2020
    refurbished_good = 2030
    refurbished_seller = 2500
    like_new = 2750
    used = 3000
    used_very_good = 4000
    used_good = 5000
    used_acceptable = 6000
    not_working_or_for_parts = 7000


class OxfamCondition(str, Enum):
    pass