import requests
from lxml import html
from fake_headers import Headers
import pprint
pp = pprint.PrettyPrinter(indent=4)

header = Headers(headers=True).generate()

#mail.ru

def get_news_mail():
    url = 'https://news.mail.ru/'
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)

    content = []
    source = []
    url_list = []

    xpath_content = f'//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text()'
    for item in root.xpath(xpath_content):
        content.append(item.replace('\xa0', ' ').replace('\r', '').replace('\n', ''))
        source.append('mail.ru')

    xpath_url = f'//a[@class="photo photo_full photo_scale js-topnews__item"]/@href'
    for a in root.xpath(xpath_url):
        url_list.append(a)

    xpath_url = '//a[@class="photo photo_small photo_scale photo_full js-topnews__item"]/@href'
    for a in root.xpath(xpath_url):
        url_list.append(a)

    for i in range(1, 9):
        xpath_content = f'/html/body/div[7]/div[2]/div[1]/div/div[2]/ul/li[{i}]/a[1]/text()'
        xpath_url = f'/html/body/div[7]/div[2]/div[1]/div/div[2]/ul/li[{i}]/a[contains(@href, "news.mail.ru")]/@href'
        for w in root.xpath(xpath_url):
            if w in url_list:
                continue
            else:
                source.append('mail.ru')
                url_list.append(w)
                for a in root.xpath(xpath_content):
                    content.append(a.replace('\xa0', ' ').replace('\r', '').replace('\n', ''))

    news = []

    for num, q in enumerate(content):
        news.append(
            {
            'Content': q,
            'Link': url_list[num],
            'Source': source[num]
            }
        )

    return news

pp.pprint(get_news_mail())

#lenta.ru

def get_news_lenta():
    url = 'https://lenta.ru/parts/news/'
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)

    content = []
    url_list = []
    source = []

    for i in range(0, 1):
        xpath_content = f'//a[contains(@href, "/news/2021/")]/text()'
        xpath_url = f'//a[contains(@href, "/news/2021/")]/@href'
        for a in root.xpath(xpath_content):
            content.append(a.replace('\xa0', ' ').replace('\r', '').replace('\n', ''))
            source.append('lenta.ru')
        for y in root.xpath(xpath_url):
            url_list.append('https://lenta.ru' + y)

    news = []

    for num, q in enumerate(content):
        news.append(
            {
            'Content': q,
            'Link': url_list[num],
            'Source': source[num]
            }
        )

    return news

pp.pprint(get_news_lenta())

#ya.ru

def get_news_ya():
    url = 'https://yandex.ru/news'
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)

    content = []
    url_list = []
    source = []

    xpath_content = '//h2[@class="mg-card__title"]/text()'
    for i in root.xpath(xpath_content):
        content.append(i.replace('\xa0', ' ').replace('\r', '').replace('\n', ''))
        source.append('yandex.ru')
    xpath_url = '//a[@class="mg-card__link"]/@href'
    for b in root.xpath(xpath_url):
        url_list.append(b)

    news = []

    for num, q in enumerate(content):
        news.append(
            {
            'Content': q,
            'Link': url_list[num],
            'Source': source[num]
            }
        )

    return news

pp.pprint(get_news_ya())
