import requests
from bs4 import BeautifulSoup
import json

class FurnitureParser:
    def __init__(self):
        self.base_url = """тут будут урлс"""
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        }

    def get_page(self, url):
        r = requests.get(url, headers=self.headers)
        return r.text if r.status_code == 200 else None

    def get_furniture_urls(self, category_urls):
        furniture_urls = []
        for category_url in category_urls:
            html = self.get_page(category_url)
            if html:
                soup = BeautifulSoup(html, "lxml")
                furniture_links = soup.select("#product-list > ul > li:nth-child(n) > a")
                furniture_urls.extend([self.base_url + link.get('href') for link in furniture_links])
        return furniture_urls

    def parse_furniture(self, url):
        html = self.get_page(url)
        if html:
            soup = BeautifulSoup(html, "lxml")
            title = soup.find("h1").get_text().replace('\n', '')
            img = self.base_url + soup.find('img').get('src').replace(' ', '')
            price = soup.find(class_='price nowrap').get_text().replace(" ", "")[:-1].replace(' ', '').replace('\r', '')
            price1 = int(price) * 0.29
            itog_price1 = round(price1 / 100) * 100
            itog_price = int(price) - itog_price1
            description = soup.find(class_='features').get_text().replace('\n', '').replace('\r', '').replace('   ', '')
            img_modul = [self.base_url + img.get("src").replace(' ', '') for img in soup.find(class_='description').find_all('img')]
            price_modul = [price.get_text().replace(' ', '') for price in soup.find_all(class_='price nowrap')]

            furniture_data = {
                'Название': title,
                'Изображение': img,
                'Цена с учетом - 29%': itog_price,
                'Полная цена': price,
                'Модуль': img_modul,
                'Цена каждого модуля': price_modul,
                'Описание': description,
            }
            return furniture_data
        return None

    def save_to_json(self, data):
        with open('svmebel.json', 'a', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

    def main(self):
        category_urls = [
            """тут будут урлс"""
        ]
        furniture_urls = self.get_furniture_urls(category_urls)

        for url in furniture_urls:
            furniture_data = self.parse_furniture(url)
            if furniture_data:
                self.save_to_json(furniture_data)

if __name__ == "__main__":
    parser = FurnitureParser()
    parser.main()
