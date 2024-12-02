import scrapy
import csv
import matplotlib.pyplot as plt


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

        # Чтение данных из CSV-файла для анализа
        prices = []
        with open('divan_data.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    # Проверяем, что цена существует и является числом
                    price = int(row['price'])
                    prices.append(price)
                except (ValueError, TypeError):
                    continue  # Пропускаем строки с некорректными данными

        if prices:
            # Вычисляем среднюю цену
            avg_price = sum(prices) / len(prices)

            # Выводим среднюю цену
            print(f"Средняя цена на диваны: {avg_price:.2f} ₽")

            # Построение гистограммы цен
            plt.hist(prices, bins=10, color='blue', alpha=0.7, edgecolor='black')
            plt.title('Гистограмма цен на диваны')
            plt.xlabel('Цена (₽)')
            plt.ylabel('Количество')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()
        else:
            print("Не удалось найти цены для анализа.")