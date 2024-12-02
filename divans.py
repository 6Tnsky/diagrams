#Необходимо спарсить цены на диваны с сайта divan.ru в csv файл, обработать данные, найти среднюю цену и
#вывести ее, а также сделать гистограмму цен на диваны
import scrapy
import csv

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla"]

    def __init__(self):
        # Открываем файл для записи данных
        self.file = open('divan_data.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file)
        # Записываем заголовки колонок
        self.csv_writer.writerow(['name', 'price', 'url'])

    def parse(self, response):
        divans = response.css('div._Ud0k')
        for divan in divans:
            name = divan.css('div.lsooF span::text').get()
            price_text = divan.css('div.pY3d2 span::text').get()

            # Удаляем пробелы между разрядами и преобразуем в число
            if price_text:
                price = int(price_text.replace(' ', '').replace('₽', '').strip())
            else:
                price = None  # Если цена отсутствует

            url = divan.css('a').attrib['href']

            # Записываем строку данных в CSV файл
            self.csv_writer.writerow([name, price, url])

            # Также возвращаем данные через yield (опционально)
            yield {
                'name': name,
                'price': price,
                'url': url
            }

    def closed(self, reason):
        # Закрываем файл после завершения работы паука
        self.file.close()