import scrapy

class Hw5sjSpider(scrapy.Spider):
    name = 'hw5sj'
    allowed_domains = ['www.superjob.ru']
    start_urls = ['https://www.superjob.ru//']
    pages_count = 10
    job = 'Python'

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://www.superjob.ru/vacancy/search/?keywords={self.job}&geo%5Bt%5D%5B0%5D=4&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath('//*[@class="_2g1F-"]/div/div[1]/div/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        temp = ''
        for i in response.xpath('//*[@class="_1OuF_ ZON4b"]//text()').extract():
            temp += i
        if temp == 'По договорённости' or len(temp) == 0:
            salary_min = 'Не указано'
            salary_max = 'Не указано'
        elif '—' not in temp:
            salary_min = temp.replace(' ', '').replace('руб./', '').replace('час', '').replace('месяц','').replace('от', '').replace('до', '')
            salary_max = temp.replace(' ', '').replace('руб./', '').replace('час', '').replace('месяц','').replace('от', '').replace('до', '')
        else: salary_min, salary_max = temp.replace(' ', '').replace('руб./', '').replace('час', '').replace('месяц','').split('—')
        if 'час' in temp:
            rate = 'руб./час'
        elif 'месяц' in temp:
            rate = 'руб./месяц'
        else:
            rate = 'Не указано'
        item = {
            'vacancy': response.xpath('/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div/h1/text()').extract(),
            'salary_max': salary_max,
            'salary_min': salary_min,
            'Rate': rate,
            'url': response.request.url,
            'site': 'SuperJob'
        }
        yield item