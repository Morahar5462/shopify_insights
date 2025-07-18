
import re
from typing import List
from urllib.parse import urljoin

async def is_valid_shopify_store(url: str) -> bool:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36"
        }
        async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
            response = await client.get(url)

        # Try different heuristics to detect Shopify
        html = response.text.lower()
        headers = response.headers

        return (
            "cdn.shopify.com" in html or
            "x-shopify-stage" in headers or
            "shopify" in html or
            "x-request-id" in headers or
            "x-shopify" in "".join(headers.keys()).lower()
        )
    except Exception as e:
        print(f"[is_valid_shopify_store ERROR] {e}")
        return False
def extract_valid_emails(text: str) -> List[str]:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = list(set(re.findall(pattern, text)))
    return [e for e in emails if not any(c.isdigit() and '.' not in e for c in e)]

def extract_valid_phone_numbers(text: str) -> List[str]:
    pattern = r'(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}'
    results = re.findall(pattern, text)
    cleaned = []
    for p in set(results):
        digits_only = re.sub(r'\D', '', p)
        if len(digits_only) >= 10:
            cleaned.append(digits_only)
    return cleaned


def extract_social_links(social_links: List[str]) -> List[str]:
    socials = ["facebook.com", "instagram.com", "twitter.com", "linkedin.com", "youtube.com"]
    return [link for link in socail_links if any(social in link.lower() for social in socials)]

