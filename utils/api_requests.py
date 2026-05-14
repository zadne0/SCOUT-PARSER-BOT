import requests
import json
from bs4 import BeautifulSoup

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
    return None

def get_crypto_price(coin="bitcoin"):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url).json()
        return response[coin]['usd']
    except:
        return "Не удалось получить курс"

# ВОТ ТУТ ОНА ДОЛЖНА БЫТЬ ОТДЕЛЬНО И С НАЧАЛА СТРОКИ:
def get_web_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # СПОСОБ №1: Ищем в JSON-LD (самый надежный для магазинов)
            json_ld = soup.find_all('script', type='application/ld+json')
            for script in json_ld:
                try:
                    data = json.loads(script.string)
                    # Ищем поле price в структуре
                    if isinstance(data, dict):
                        if 'offers' in data:
                            offers = data['offers']
                            if isinstance(offers, dict) and 'price' in offers:
                                return f"{offers['price']} {offers.get('priceCurrency', 'BYN')}"
                        elif '@graph' in data: # Для сложных структур
                            for item in data['@graph']:
                                if 'offers' in item:
                                    return f"{item['offers']['price']} BYN"
                except: continue

            # СПОСОБ №2: Специфические классы 5 Элемента
            if "5element.by" in url:
                price_tag = soup.find('meta', itemprop='price')
                if price_tag:
                    return f"{price_tag['content']} BYN"

            return "Цена не найдена (сайт блокирует бота)"
        return f"Ошибка сайта: {response.status_code}"
    except Exception as e:
        return f"Ошибка: {e}"
