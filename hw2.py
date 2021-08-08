from bs4 import BeautifulSoup
import pandas as pd
import requests
import lxml
from fake_headers import Headers

header = Headers(headers=True).generate()

page = int(input('Введите количество страниц:'))
work = input('Введите вакансию:')

url_list_hh = []
url_list = []
vacancy = []
employeur = []
salary = []
site = []

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

all_vacancy_info = []

for num, q in enumerate(vacancy):
   all_vacancy_info.append({
       'Vacancy': q,
       'Employeur': employeur[num],
       'Salary': salary[num],
       'Site': site[num],
       'url': url_list[num]
   })

print(all_vacancy_info)
pd.DataFrame(all_vacancy_info).to_csv('dump.csv', encoding='utf-8-sig')
