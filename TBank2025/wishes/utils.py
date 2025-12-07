import requests
import re
import json
from bs4 import BeautifulSoup
from decimal import Decimal


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }


def parse_wb(url):
    try:
        regex = r"catalog/(\d+)/detail"
        match = re.search(regex, url)

        if not match:
            return None

        item_id = match.group(1)

        api_url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}"

        response = requests.get(api_url, headers=get_headers())
        data = response.json()

        product = data['data']['products'][0]

        title = product.get('name', '')
        price = product.get('salePriceU') or product.get('priceU')
        price = Decimal(price) / 100

        category = "Wildberries"

        return {
            "title": title,
            "price": price,
            "category": category
        }
    except Exception as e:
        print(f"Error parsing WB: {e}")
        return None

def parse_generic(url):

    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        title = ""
        price = 0

        og_title = soup.find("meta", property="og:title")
        if og_title:
            title = og_title.get("content")
        else:
            title = soup.title.string if soup.title else ""

        og_price = soup.find("meta", property="product:price:amount")
        ya_price = soup.find("meta", itemprop="price")

        price_str = None
        if og_price:
            price_str = og_price.get("content")
        elif ya_price:
            price_str = ya_price.get("content")

        if price_str:
            clean_price = re.sub(r'[^\d.]', '', price_str)
            price = Decimal(clean_price)

        return {
            "title": title.strip(),
            "price": price,
            "category": "Другое"
        }
    except Exception as e:
        print(f"Error parsing generic: {e}")
        return None


def get_product_info(url):
    if "wildberries" in url or "wb.ru" in url:
        result = parse_wb(url)
        if result: return result

    return parse_generic(url)