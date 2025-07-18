

'''from bs4 import BeautifulSoup
from utils.helpers import (
    extract_valid_emails,
    extract_valid_phone_numbers,
    extract_social_links,
    clean_policy_link
)
import httpx
import re
from urllib.parse import urlparse

async def scrape_shopify_store(url: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator="\n", strip=True)
        links = [a.get("href", "") for a in soup.find_all("a", href=True)]

        # 1. Product catalog from /products.json
        base = url.rstrip("/")
        catalog_url = f"{base}/products.json"
        try:
            catalog_resp = await client.get(catalog_url)
            all_products = catalog_resp.json().get("products", [])
        except Exception:
            all_products = []

        # 2. Hero Products from Home Page
        hero_products = []
        product_classes = re.compile(r"(product-card|product-item|grid__item|featured|bestseller)", re.IGNORECASE)
        hero_tags = soup.find_all(class_=product_classes)
        for tag in hero_tags:
            title_tag = tag.find(["h2", "h3", "span"])
            img_tag = tag.find("img")
            title = title_tag.get_text(strip=True) if title_tag else None
            image = img_tag.get("src") if img_tag and img_tag.has_attr("src") else None
            if title:
                hero_products.append({"title": title, "image": image})

        # Fallback: use all <img alt=...> tags as pseudo-products
        if not hero_products:
            for img_tag in soup.find_all("img"):
                alt = img_tag.get("alt")
                if alt and len(alt.split()) > 1:
                    hero_products.append({
                        "title": alt.strip(),
                        "image": img_tag.get("src")
                    })

        policies = {}
        policy_keywords = ['return', 'refund', 'shipping', 'cancellation', 'privacy', 'terms']
    
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            for keyword in policy_keywords:
                if keyword in href and href not in policies:
                    full_url = href if href.startswith('http') else base_url.rstrip('/') + '/' + href.lstrip('/')
                    try:
                        res = httpx.get(full_url, timeout=10)
                        if res.status_code == 200:
                            policy_soup = BeautifulSoup(res.text, 'html.parser')
                            policies[keyword] = policy_soup.get_text(separator='\n', strip=True)[:1000]  # limit to 1000 chars
                    except:
                        continue
                      
        socials = {}
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "instagram.com" in href:
                socials['instagram'] = href
            elif "facebook.com" in href:
                socials['facebook'] = href
            elif "tiktok.com" in href:
                socials['tiktok'] = href
            elif "twitter.com" in href:
                socials['twitter'] = href
            elif "linkedin.com" in href:
                socials['linkedin'] = href
        # 3. Extract FAQs
        faqs = []
        faq_blocks = soup.find_all(["p", "div", "li"])
        for block in faq_blocks:
            txt = block.get_text(separator=" ").strip()
            match = re.match(r"(?i)Q[:\)]\s*(.+?)\?\s*A[:\)]\s*(.+)", txt)
            if match:
                question, answer = match.groups()
                faqs.append({"question": question.strip(), "answer": answer.strip()})

        # Fallback: Raw FAQ scanner
        if not faqs:
            matches = re.findall(r"(Q[:\)]\s?.+?\?\s*A[:\)]\s?.+?)(?=\n|$)", text, flags=re.IGNORECASE)
            for line in matches:
                parts = re.split(r"A[:\)]\s?", line, maxsplit=1)
                if len(parts) == 2:
                    question = parts[0].strip().lstrip("Q:").strip()
                    answer = parts[1].strip()
                    faqs.append({"question": question, "answer": answer})

        # Collect meta description
        description = None
        desc_tag = soup.find("meta", {"name": "description"}) or soup.find("meta", {"property": "og:description"})
        if desc_tag:
            description = desc_tag.get("content", "").strip()
        
        
        # ✅ Final result dict
        return {
            "url": url,
            "name": soup.title.text.strip() if soup.title else None,
            "description": description,
            "emails": extract_valid_emails(response.text),
            "phones": extract_valid_phone_numbers(response.text),  # Add country code inside helper if needed
            "products": all_products,
            "hero_products": hero_products,
            "faqs": faqs,
            "policies":policies,
            "socials":socials,
            
        }
'''
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import httpx

from models.schema import WebsiteResponse

def extract_social_links(soup) -> dict:
    social_links = {
        "instagram": None,
        "facebook": None,
        "tiktok": None,
        "youtube": None,
        "twitter": None,
        "linkedin": None,
        "pinterest": None
    }

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "instagram.com" in href and not social_links["instagram"]:
            social_links["instagram"] = href
        elif "facebook.com" in href and not social_links["facebook"]:
            social_links["facebook"] = href
        elif "tiktok.com" in href and not social_links["tiktok"]:
            social_links["tiktok"] = href
        elif "youtube.com" in href and not social_links["youtube"]:
            social_links["youtube"] = href
        elif "twitter.com" in href and not social_links["twitter"]:
            social_links["twitter"] = href
        elif "linkedin.com" in href and not social_links["linkedin"]:
            social_links["linkedin"] = href
        elif "pinterest.com" in href and not social_links["pinterest"]:
            social_links["pinterest"] = href

    return {k: v for k, v in social_links.items() if v}
def extract_important_links(soup, base_url):
    links = {}
    keywords = {
        "order tracking": "order_tracking",
        "track order": "order_tracking",
        "contact us": "contact",
        "blog": "blog",
        "support": "support"
    }

    for a in soup.find_all('a', href=True):
        text = a.get_text().strip().lower()
        for key in keywords:
            if key in text:
                name = keywords[key]
                href = a['href']
                links[name] = href if href.startswith('http') else base_url.rstrip('/') + '/' + href.lstrip('/')
    return links

async def scrape_shopify_store(url: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        try:
            response = await client.get(base_url)
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to fetch the homepage: {e}")

        soup = BeautifulSoup(response.text, "html.parser")
        # after soup = BeautifulSoup(response.text, "html.parser")
        social_links = extract_social_links(soup)
        important_links=extract_important_links(soup, base_url)
        # Title and description
        title = soup.title.string.strip() if soup.title else ""
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag and desc_tag.has_attr("content") else ""

        # Contact Details
        emails = list(set(re.findall(r"[\w\.-]+@[\w\.-]+", response.text)))
        phones = list(set(re.findall(r"\+?\d[\d\s\-()]{8,}\d", response.text)))

        # Extract all <a> tags
        links = soup.find_all("a", href=True)
        
        
        
        

        
        # Try to fetch products.json
        products = []
        try:
            products_url = urljoin(base_url, "/products.json")
            prod_resp = await client.get(products_url)
            prod_resp.raise_for_status()
            prod_data = prod_resp.json()
            products = prod_data.get("products", [])
        except Exception:
            pass

        # Attempt to find hero products (e.g., featured on homepage)
        hero_products = []
        product_links = soup.select('a[href*="/products/"]')
        seen = set()

        for link in product_links:
            href = link.get("href")
            full_url = urljoin(base_url, href)

    # Remove duplicates
            if full_url in seen:
                continue
            seen.add(full_url)

    # Try to extract image and title if available
            title = link.get("title") or link.text.strip() or "Untitled"
            image_tag = link.find("img")
            image = image_tag.get("src") if image_tag else None

    # Construct valid HeroProduct dict
            hero_products.append({
                    "title": title,
                    "image": urljoin(base_url, image) if image else None
            })

        # Try to fetch FAQ page
            

        return {
            "url": base_url,
            "name": title,
            "description": description,
            "emails": emails,
            "phones": phones,
            "products": products,
            "hero_products": hero_products,
            "social_links": social_links,
            "important_links": important_links,
           
        }



