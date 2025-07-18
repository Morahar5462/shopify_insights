
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict


class FAQ(BaseModel):
    question: str
    answer: str


class HeroProduct(BaseModel):
    title: str
    image: Optional[str] = None

class WebsiteRequest(BaseModel):
    url: HttpUrl
class WebsiteResponse(BaseModel):
    url: HttpUrl
    name: Optional[str]
    description: Optional[str]
    emails: List[str]=[]
    phones: List[str]=[]
    products: List[Dict]=[]
    hero_products: List[HeroProduct]=[]
    social_links: Optional[dict]
    important_links: Optional[dict]
