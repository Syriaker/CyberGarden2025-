import requests
import re
import json
from bs4 import BeautifulSoup
from decimal import Decimal


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
    }

def get_wb_image_url(item_id):
    try:
        _id = int(item_id)
        vol = _id // 100000
        part = _id // 1000
        basket = "01"

        if 0 <= vol <= 143: basket = "01"
        elif 144 <= vol <= 287: basket = "02"
        elif 288 <= vol <= 431: basket = "03"
        elif 432 <= vol <= 719: basket = "04"
        elif 720 <= vol <= 1007: basket = "05"
        elif 1008 <= vol <= 1061: basket = "06"
        elif 1062 <= vol <= 1115: basket = "07"
        elif 1116 <= vol <= 1169: basket = "08"
        elif 1170 <= vol <= 1313: basket = "09"
        elif 1314 <= vol <= 1601: basket = "10"
        elif 1602 <= vol <= 1655: basket = "11"
        elif 1656 <= vol <= 1919: basket = "12"
        elif 1920 <= vol <= 2045: basket = "13"
        elif 2046 <= vol <= 2189: basket = "14"
        elif 2190 <= vol <= 2405: basket = "15"
        else: basket = "16"

        return f"https://basket-{basket}.wb.ru/vol{vol}/part{part}/{_id}/images/big/1.webp"
    except:
        return None


def parse_wb(url):
    try:
        regex = r"catalog/(\d+)/detail"
        match = re.search(regex, url)
        if not match: return None

        item_id = match.group(1)

        api_url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}"

        response = requests.get(api_url, headers=get_headers(), timeout=10)
        data = response.json()
        products = data.get('data', {}).get('products', [])

        if not products: return None
        product = products[0]

        title = product.get('name', '')

        price_kopecks = product.get('salePriceU') or product.get('priceU')
        if not price_kopecks and 'sizes' in product:
            for size in product['sizes']:
                if size.get('price'):
                    price_kopecks = size['price'].get('total') or size['price'].get('basic')
                    if price_kopecks: break
                elif size.get('salePriceU') or size.get('priceU'):
                    price_kopecks = size.get('salePriceU') or size.get('priceU')
                    break

        if not price_kopecks: return None
        price = Decimal(price_kopecks) / 100

        category = product.get('subjectName') or product.get('subjectRootName') or product.get('brand', 'Wildberries')

        image_url = get_wb_image_url(item_id)

        return {
            "title": title,
            "price": price,
            "category": category,
            "image_url": image_url
        }
    except Exception as e:
        print(f"❌ [WB Error] {e}")
        return None

def parse_generic(url):
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        if response.status_code not in [200, 404]: return None

        soup = BeautifulSoup(response.text, 'html.parser')

        title = ""
        og_title = soup.find("meta", property="og:title")
        if og_title:
            title = og_title.get("content")
        elif soup.title:
            title = soup.title.string

        title = title.replace(" — купить по низкой цене на Яндекс Маркете", "").strip()

        if title in ["Яндекс Маркет", "Ой!", "Captcha", "Security Check"]: return None

        price = 0
        meta_prices = [
            soup.find("meta", property="product:price:amount"),
            soup.find("meta", itemprop="price"),
            soup.find("meta", property="ya:price")
        ]
        for meta in meta_prices:
            if meta and meta.get("content"):
                try:
                    raw = meta.get("content").replace(',', '.').replace(u'\xa0', '')
                    price = Decimal(re.sub(r'[^\d.]', '', raw))
                    if price > 0: break
                except:
                    continue

        if price <= 0: return None

        image_url = None
        og_image = soup.find("meta", property="og:image")
        if og_image:
            image_url = og_image.get("content")

        return {
            "title": title,
            "price": price,
            "category": "Другое",
            "image_url": image_url
        }
    except Exception as e:
        print(f"❌ [Generic Error] {e}")
        return None


def get_product_info(url):
    if "wildberries" in url or "wb.ru" in url:
        return parse_wb(url)
    return parse_generic(url)

def get_product_info(url):
    if "wildberries" in url or "wb.ru" in url:
        return parse_wb(url)
    return parse_generic(url)