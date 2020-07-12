# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pymongo import MongoClient
from pprint import pprint

import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')  #--headless

driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')

elem.send_keys(Keys.ENTER)
time.sleep(0.7)

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')

elem.send_keys(Keys.ENTER)

time.sleep(4)

mails_list = []

last_mail = None
while True:
    mails = driver.find_elements_by_class_name('js-letter-list-item')
    for mail in mails:
        mail_url = mail.get_attribute('href')
        if mail_url not in mails_list:
            mails_list.append(mail_url)
    if mails[-1] != last_mail:
        last_mail = mails[-1]
        actions = ActionChains(driver)
        actions.move_to_element(mails[-1])
        actions.perform()
    else:
        break

for mail in mails_list:
    page = driver.get(mail)
    time.sleep(3)
    mails_data = {}
    try:
        contact = driver.find_element_by_class_name('letter-contact')
        contact = contact.get_attribute('title')
    except:
        pass

    try:
        date = driver.find_element_by_class_name('letter__date').text
    except:
        pass

    try:
        topic = driver.find_element_by_class_name('thread__subject-line').text
    except:
        pass

    try:
        text = driver.find_element_by_class_name('letter__body').text
    except:
        pass

    mails_data['contact'] = contact
    mails_data['date'] = date
    mails_data['topic'] = topic
    mails_data['text'] = text
    mails.append(mails_data)

pprint(mails)
print(len(mails))

client = MongoClient('localhost', 27017)
db = client['mails']
db.mails.delete_many({})
db.mails.insert_many(mails_list)

driver.quit()
