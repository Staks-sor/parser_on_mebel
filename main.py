import requests
from bs4 import BeautifulSoup
import lxml
import time
import json
import csv

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
}


def get_lerom(url):
    r = requests.get(url=url, headers=headers)
    return r


def get_content(html):

    url_list = ["https://svmebel-vrn.ru/category/gostinye/", "https://svmebel-vrn.ru/category/detskie/", "https://svmebel-vrn.ru/category/spalni/", "https://svmebel-vrn.ru/category/prikhozhie/"]

    for url in url_list:
        r = requests.get(str(url))
        soup = BeautifulSoup(r.text, "lxml")
        model = soup.select("#product-list > ul > li:nth-child(n) > a")
        # model = soup.find_all(class_="thumbs product-list")
        # print(model)

        for item in model:
            url_list1 = []
            url_list1.extend([('https://svmebel-vrn.ru' + item.get('href'))])
            # print(url_list1)
            for url1 in url_list1:
                r = requests.get(str(url1))
                soup = BeautifulSoup(r.text, "lxml")
                model1 = soup.find_all(class_="content")

                for item_content in model1:
                    title = item_content.find('h1').get_text().replace('\n', '')
                    img = 'https://svmebel-vrn.ru' + item_content.find('img').get('src').replace(' ', '')
                    price = item_content.find(class_='price nowrap').get_text().replace(" ", "")[:-1].replace(' ', '').replace('\r', '')
                    price1 = int(price) * 0.29
                    itog_price1 = round(price1 / 100) * 100
                    itog_price = int(price) - itog_price1

                    opis = item_content.find(class_='features').get_text().replace('\n', '').replace('\r', '').replace('   ', '')

                    try:
                        img_modul = item_content.find(class_='description').find_all('img')
                    except AttributeError:
                        continue
                    print("Нет модуля")
                    price_modul = item_content.find_all(class_='price nowrap')

                    mod = ("    ".join(
                        str('https://svmebel-vrn.ru' + i.get("src").replace(' ', ''))
                        for i in img_modul))
                    mod_price = ("    ".join(
                        str(i.get_text().replace(' ', ''))
                        for i in price_modul))


                    print(title, img, '\n', 'цена с вычетом процента: ', int(price) - price1, "₽", '\n', 'цена ориг: ', price, "₽", "\n", mod, '\n', mod_price, '\n', opis)


                    data = {
                        'Название': title,
                        'Изображение': img,
                        'Цена с учетом - 29%': itog_price,
                        'Полная цена': price,
                        'Модуль': mod,
                        'Цена каждого модуля': mod_price,
                        'Описание': opis,
                    }
                    with open('svmebel.json', 'a', encoding='utf-8') as outfile:
                        json.dump(data, outfile, indent=4, ensure_ascii=False)




def main():

        url_gag = "https://svmebel-vrn.ru"

        html = get_lerom(url_gag)
        if html.status_code == 200:
            get_content(html.text)
        else:
            print("ERROR")




if __name__ == "__main__":
    main()
