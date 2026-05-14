import requests
from bs4 import BeautifulSoup

def get_price_from_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Это заготовка, логику под конкретный сайт (теги) допишем чуть позже
        return response.status_code 
    except Exception as e:
        return f"Ошибка парсинга: {e}"