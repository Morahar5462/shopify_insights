

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import HttpUrl
from models.schema import WebsiteRequest, WebsiteResponse
from utils.helpers import is_valid_shopify_store
from utils.scraper import scrape_shopify_store

app = FastAPI(title="Shopify Store Insights API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Shopify Store Insights API!",
        "usage": {
            "GET": "/analyze?url=https://www.tentree.com",
            "POST": "/fetch-insights with JSON body: { 'website_url': 'https://www.tentree.com' }"
        }
    }

@app.get("/analyze")
async def analyze_shopify_store(url: str = Query(..., description="The full Shopify store URL")):

    if not await is_valid_shopify_store(url):
        raise HTTPException(status_code=401, detail="Website not reachable or not a valid Shopify store")

    try:
        result = await scrape_shopify_store(url)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fetch-insights", response_model=WebsiteResponse)
async def fetch_insights(payload: WebsiteRequest):
    web_url = str(payload.url)
     # TEMP: Bypass Shopify store check
   # if not await is_valid_shopify_store(url):
    #    raise HTTPException(status_code=401, detail="Website not reachable or not a valid Shopify store")

    try:
        result = await scrape_shopify_store(web_url)
        return WebsiteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

