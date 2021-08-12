from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import lxml
from fake_headers import Headers
import pprint
pp = pprint.PrettyPrinter(indent=4)

client = MongoClient('localhost', 27017)
db = client.vacancy
collection = db.vac

header = Headers(headers=True).generate()

page = int(input('Введите количество страниц:'))
work = input('Введите вакансию:')

url_list_hh = []
url_list = []
vacancy = []
employeur = []
salary = []
site = []

def digitization(a):
    import re
    a = [re.split(' до | — ', i) for i in a]
    b = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    c = []
    for i in a:
        r = []
        for p in i:
            if p == 'з/п не указана' or p == 'По договорённости':
                r.append(p)
                continue
            elif p == 'вычета налогов' or p == '':
                continue
            else:
                o = ''
                for x in p:
                    if x not in b:
                        pass
                    else:
                        o += x
            o = int(o)
            r.append(o)
        c.append(r)
    return c

def digit_filter(a):
    maximum = []
    minimum = []
    for i in a:
        if len(i) == 0:
            continue
        elif len(i) == 1:
            maximum.append(i[0])
            minimum.append(i[0])
        elif i[0] > i[1]:
            maximum.append(i[0])
            minimum.append(i[1])
        else:
            maximum.append(i[1])
            minimum.append(i[0])
    return maximum, minimum

#Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
def print_salary(salary):
    objects = collection.find({'Max_salary': {'$gt': salary}})
    for obj in objects:
        pp.pprint(obj)

for x in range(0, page):
    url_hh = f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={work}&area=113&page={x}'
    response_hh = requests.get(url_hh, headers=header)
    soup_hh = BeautifulSoup(response_hh.text, 'lxml')
    for i in soup_hh.select('[data-qa="vacancy-serp__vacancy-title"]'):
        url_list_hh.append(i['href'])
        url_list.append(i['href'])
        site.append('HeadHunter')

for i in url_list_hh:
    url_temp = i
    response_temp = requests.get(url_temp, headers=header)
    soup_temp = BeautifulSoup(response_temp.text, 'lxml')

    for z in soup_temp.select('[data-qa="vacancy-title"]'):
        vacancy.append(z.text.replace('\xa0', ' '))
    for y in soup_temp.select('a.vacancy-company-name'):
        employeur.append(y.text.replace('\xa0', ' '))
    for o in soup_temp.select('p.vacancy-salary'):
        salary.append(o.text.replace('\xa0', ' '))


url_list_sj = []

for x in range(0, page):
    url_sj = f'https://russia.superjob.ru/vacancy/search/?keywords={work}&page={x}'
    response_sj = requests.get(url_sj, headers=header)
    soup_sj = BeautifulSoup(response_sj.text, 'lxml')
    for i in soup_sj.select('._1h3Zg._2rfUm._2hCDz._21a7u a'):
        url_iter = 'https://russia.superjob.ru/' + i['href']
        url_list_sj.append(url_iter)
        url_list.append(url_iter)
        site.append('SuperJob')

for i in url_list_sj:
    url_temp = i
    response_temp = requests.get(url_temp, headers=header)
    soup_temp = BeautifulSoup(response_temp.text, 'lxml')

    for w in soup_temp.select('h1'):
        vacancy.append(w.text.replace('\xa0', ' '))
    for e in soup_temp.select('._2g1F- a h2'):
        employeur.append(e.text.replace('\xa0', ' '))
    for r in soup_temp.select('._1OuF_.ZON4b'):
        salary.append(r.text.replace('\xa0', ' '))

salary = digitization(salary)

max_salary, min_salary = digit_filter(salary)

for num, q in enumerate(vacancy):
    # Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
    if bool(collection.find_one({'url': { "$in": [url_list[num]]}})) == True:
        continue
    else:
        collection.insert_one(
            {
            'Vacancy': q,
            'Employeur': employeur[num],
            'Max_salary': max_salary[num],
            'Min_salary': min_salary[num],
            'Site': site[num],
            'url': url_list[num]
            }
        )


#Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
print_salary(100000)