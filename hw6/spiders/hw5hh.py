import scrapy

class Hw5hhSpider(scrapy.Spider):
    name = 'hw5hh'
    allowed_domains = ['hh.ru/']
    start_urls = ['https://hh.ru//']
    pages_count = 10
    job = 'Python'

    def start_requests(self):
        for page in range(0, self.pages_count):
            url = f'https://hh.ru/search/vacancy?area=113&fromSearchLine=true&st=searchVacancy&text={self.job}&from=suggest_post&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        link = []
        vacancy = []
        salary_min = []
        salary_max = []

        for i in response.xpath('//*[@data-qa="vacancy-serp__vacancy-title"]/@href').extract():
            link.append(i)
        for vac in response.xpath('//*[@data-qa="vacancy-serp__vacancy-title"]/text()').extract():
            vacancy.append(vac.strip().replace(' ', ' '))
        for sal in response.xpath('//*[@data-qa="vacancy-serp__vacancy-compensation"]/text()').extract():
            sal = sal.replace(' ', '').replace(' ', '')
            if '–' in sal:
                sal_min, sal_max = sal.split('–')
                salary_min.append(sal_min)
                salary_max.append(sal_max)
            else:
                salary_max.append(sal)
                salary_min.append(sal)

        if len(salary_min) != len(vacancy):
            salary_min.append('Не указана')
            salary_max.append('Не указана')
        else:
            pass

        for num, q in enumerate(vacancy):
            item = {
                'vacancy': q,
                'salary_min': salary_min[num],
                'salary_max': salary_max[num],
                'url': link[num],
                'site': 'HeadHunter'
                }
            yield item