# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


def process_price(price):
    price = int(price[2].replace(' ', ''))
    return price


def process_currency(currency):
    currency = currency[0].strip()[:-1]
    return currency


def process_photo(photos):
    photos = ["https://castorama.ru" + photo for photo in photos if photo[0] == "/"]
    return photos

def process_name(name):
    name = name[0].strip()
    return name


class CastoramaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    currency = scrapy.Field(input_processor=Compose(process_currency), output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=Compose(process_photo))
    url = scrapy.Field(output_processor=TakeFirst())
