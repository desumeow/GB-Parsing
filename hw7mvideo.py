from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.firefox.options import Options

client = MongoClient('localhost', 27017)
db = client.mvideo
collection = db.top

options = Options()
options.binary_location = r'C:\Users\Desu_Vult\AppData\Local\Mozilla Firefox\firefox.exe'

driver = webdriver.Firefox(executable_path=r'C:\WebDrivers\geckodriver.exe', options=options)

url = 'https://www.mvideo.ru/'
title_site = 'МВидео'

driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="c-popup__close u-sticky"]')))
button_close = driver.find_element_by_xpath('//*[@class="c-popup__close u-sticky"]')
button_close.click()

next_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/a[2]')))

count_next = 0
while count_next < 500:
    driver.execute_script("$(arguments[0]).click();", next_button)
    count_next += 1

prev_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/a[1]')))

count_prev = 0
while count_prev < 500:
    driver.execute_script("$(arguments[0]).click();", prev_button)
    count_prev += 1


for a in range(1, 16):
    collection.insert_one(
        {
            'Product': driver.find_element_by_xpath(
                f'/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/div/ul/li[{a}]/div/div[3]/div/div/h3').get_attribute('innerText'),
            'Price': driver.find_element_by_xpath(
                f'/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/div/ul/li[{a}]/div/div[5]/div[1]/div/span[1]').get_attribute('innerText'),
            'URL': driver.find_element_by_xpath(f'/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/div/ul/li[{a}]/div/div[3]/div/div/h3/a').get_attribute('href')
        }
    )

driver.quit()
