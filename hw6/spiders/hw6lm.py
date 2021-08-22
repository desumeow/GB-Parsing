import scrapy
from scrapy.loader import ItemLoader
from ..items import ImgHW6Item

class Hw6lmSpider(scrapy.Spider):
    name = 'hw6lm'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/osveshchenie/?page=1']
    pages_count = 2

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://leroymerlin.ru/catalogue/osveshchenie/?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath('//section/div/div/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        tech = {}
        term = []
        definition = []
        for i in response.xpath('//*[@class="def-list__term"]/text()').extract():
            term.append(i)
        for b in response.xpath('//*[@class="def-list__definition"]/text()').extract():
            definition.append(b.replace('  ', '').replace('\n', ''))
        for t, d in zip(term, definition):
            tech[f'{t}'] = f'{d}'

        f = ItemLoader(item=ImgHW6Item(), response=response)
        f.add_xpath('file_name', '//*[@class="header-2"]/text()')
        f.add_xpath('price', '//span[@slot="price"]/text()')
        f.add_value('techs', tech)
        f.add_xpath('file_urls', '//uc-pdp-media-carousel/picture/img/@src')
        return f.load_item()

