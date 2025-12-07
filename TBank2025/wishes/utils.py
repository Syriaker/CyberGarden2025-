import requests
import re
import json
from bs4 import BeautifulSoup
from decimal import Decimal


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9',
    }

def get_wb_basket_number(item_id):
    try:
        _id = int(item_id)
        vol = _id // 100000
        part = _id // 1000
        basket = "01"

        if 0 <= vol <= 143:
            basket = "01"
        elif 144 <= vol <= 287:
            basket = "02"
        elif 288 <= vol <= 431:
            basket = "03"
        elif 432 <= vol <= 719:
            basket = "04"
        elif 720 <= vol <= 1007:
            basket = "05"
        elif 1008 <= vol <= 1061:
            basket = "06"
        elif 1062 <= vol <= 1115:
            basket = "07"
        elif 1116 <= vol <= 1169:
            basket = "08"
        elif 1170 <= vol <= 1313:
            basket = "09"
        elif 1314 <= vol <= 1601:
            basket = "10"
        elif 1602 <= vol <= 1655:
            basket = "11"
        elif 1656 <= vol <= 1919:
            basket = "12"
        elif 1920 <= vol <= 2045:
            basket = "13"
        elif 2046 <= vol <= 2189:
            basket = "14"
        elif 2190 <= vol <= 2405:
            basket = "15"
        elif 2406 <= vol <= 2613:
            basket = "16"
        elif 2614 <= vol <= 2821:
            basket = "17"
        elif 2822 <= vol <= 3029:
            basket = "18"
        elif 3030 <= vol <= 3237:
            basket = "19"
        elif 3238 <= vol <= 3445:
            basket = "20"
        elif 3446 <= vol <= 3653:
            basket = "21"
        elif 3654 <= vol <= 3861:
            basket = "22"
        elif 3862 <= vol <= 4069:
            basket = "23"
        elif 4070 <= vol <= 4277:
            basket = "24"
        elif 4278 <= vol <= 4485:
            basket = "25"
        elif 4486 <= vol <= 4693:
            basket = "26"
        elif 4694 <= vol <= 4901:
            basket = "27"
        elif 4902 <= vol <= 5109:
            basket = "28"
        elif 5110 <= vol <= 5317:
            basket = "29"
        elif 5318 <= vol <= 5525:
            basket = "30"
        elif 5526 <= vol <= 5733:
            basket = "31"
        elif 5734 <= vol <= 5941:
            basket = "32"
        else:
            basket = "33"

        return basket, vol, part
    except:
        return None, None, None

def parse_wb(url):
    try:
        regex = r"catalog/(\d+)/detail"
        match = re.search(regex, url)
        if not match: return None
        item_id = match.group(1)

        basket, vol, part = get_wb_basket_number(item_id)
        if not basket: return None

        price = 0
        title = ""
        category = "Wildberries"

        api_url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}"
        resp_price = requests.get(api_url, headers=get_headers(), timeout=5)

        if resp_price.status_code == 200:
            data = resp_price.json()
            products = data.get('data', {}).get('products', [])
            if products:
                prod = products[0]
                title = prod.get('name', '')

                price_kopecks = prod.get('salePriceU') or prod.get('priceU')
                if not price_kopecks and 'sizes' in prod:
                    for size in prod['sizes']:
                        if size.get('price'):
                            price_kopecks = size['price'].get('total') or size['price'].get('basic')
                            if price_kopecks: break
                        elif size.get('salePriceU') or size.get('priceU'):
                            price_kopecks = size.get('salePriceU') or size.get('priceU')
                            break
                if price_kopecks:
                    price = Decimal(price_kopecks) / 100

        if price == 0:
            print("❌ [WB] Не удалось найти цену")
            return None

        domains = ['wb.ru', 'wbbasket.ru']
        active_host = None

        for domain in domains:
            try:
                test_host = f"basket-{basket}.{domain}"
                info_url = f"https://{test_host}/vol{vol}/part{part}/{item_id}/info/ru/card.json"

                resp_info = requests.get(info_url, headers=get_headers(), timeout=3)

                if resp_info.status_code == 200:
                    active_host = test_host
                    info_data = resp_info.json()
                    category = info_data.get('subj_name') or info_data.get('subj_root_name') or category
                    if not title:
                        title = info_data.get('imt_name') or ""
                    break
            except Exception:
                continue

        if not title: title = "Товар Wildberries"

        image_url = None
        if active_host:
            image_url = f"https://{active_host}/vol{vol}/part{part}/{item_id}/images/big/1.webp"
        else:
            image_url = f"https://basket-{basket}.wbbasket.ru/vol{vol}/part{part}/{item_id}/images/big/1.webp"

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
        if title: title = title.replace(" — купить по низкой цене на Яндекс Маркете", "").strip()
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

        category = "Другое"
        meta_cat = soup.find("meta", property="article:section")
        meta_prod_cat = soup.find("meta", property="product:category")
        if meta_cat and meta_cat.get("content"):
            category = meta_cat.get("content")
        elif meta_prod_cat and meta_prod_cat.get("content"):
            category = meta_prod_cat.get("content")

        image_url = None
        og_image = soup.find("meta", property="og:image")
        if og_image: image_url = og_image.get("content")

        return {
            "title": title,
            "price": price,
            "category": category,
            "image_url": image_url
        }
    except Exception as e:
        print(f"❌ [Generic Error] {e}")
        return None


def get_product_info(url):
    if "wildberries" in url or "wb.ru" in url:
        return parse_wb(url)
    return parse_generic(url)