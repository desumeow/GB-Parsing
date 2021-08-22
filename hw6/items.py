# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose

def cleaner_url(url):
    if url[:2] == '//':
        return f'https:{url}'
    return url

def digitization(digit):
    d = ''
    for i in digit:
        if i.isdigit() == True:
            d += i
        else:
            pass
    digit = int(d)
    return digit


class ImgHW6Item(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field(input_processor=MapCompose(cleaner_url))
    price = scrapy.Field(input_processor=MapCompose(digitization))
    techs = scrapy.Field()
    file_name = scrapy.Field(
        output_processor=TakeFirst()
    )