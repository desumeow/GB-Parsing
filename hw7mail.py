from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.firefox.options import Options

client = MongoClient('localhost', 27017)
db = client.mail
collection = db.mails

options = Options()
options.binary_location = r'C:\Users\Desu_Vult\AppData\Local\Mozilla Firefox\firefox.exe'

driver = webdriver.Firefox(executable_path=r'C:\WebDrivers\geckodriver.exe', options=options)

url = 'https://ya.ru/'
title_site = 'Яндекс'

driver.get(url)

username = 'username'
password = 'password'

login_button = driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td/div/a/div')
login_button.click()
login_button_2 = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[4]/a[2]')
login_button_2.click()

login_field = driver.find_element_by_xpath('//*[@id="passp-field-login"]')
continue_button = driver.find_element_by_xpath('//*[@id="passp:sign-in"]')

login_field.send_keys(f'{username}')
continue_button.click()

pass_field = driver.find_element_by_xpath('//*[@id="passp-field-passwd"]')
continue_button = driver.find_element_by_xpath('//*[@id="passp:sign-in"]')

pass_field.send_keys(f'{password}')
continue_button.click()

mail_count = 10

sender_list = []
date_list = []
subj_list = []
content_list = []

for i in range(1, 1 + mail_count):
    mail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@class="ns-view-container-desc mail-MessagesList js-messages-list"]/div[{i}]')))
    mail.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="mail-Message-Sender"]/span[1]')))
    sender_list.append(driver.find_element_by_xpath('//*[@class="mail-Message-Sender"]/span[1]').text)
    date_list.append(driver.find_element_by_xpath('//*[@class="mail-Message-Head-Floor mail-Message-Head-Floor_top"]/div[3]').text)
    subj_list.append(driver.find_element_by_xpath('//*[@class="mail-Message-Toolbar-Subject-Wrapper"]/div').text)
    content_list.append(driver.find_element_by_xpath('//*[@class="js-message-body-content mail-Message-Body-Content"]').text)
    driver.back()

for num, q in enumerate(sender_list):
    collection.insert_one(
        {
        'Sender': q,
        'Date': date_list[num],
        'Subject': subj_list[num],
        'Content': content_list[num]
        }
    )

driver.quit()