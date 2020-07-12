# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from pprint import pprint

import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')

goods_list = None
goods = driver.find_elements_by_xpath("//div[@data-init='gtm-push-products']")
for good in goods:
    if good.find_element_by_tag_name('div').text == 'Хиты продаж':
        goods_list = good
        actions = ActionChains(driver)
        actions.move_to_element(goods_list)
        actions.perform()

        break
i = True
goods_count = 0
while i:
    time.sleep(0.2)
    button = goods_list.find_element_by_class_name('sel-hits-button-next')
    actions.move_to_element(button)
    actions.click()
    actions.perform()
    try:
        goods_list.find_element_by_css_selector("a.next-btn.sel-hits-button-next.disabled")
        print('Все страницы просмотрены')
        i = False
    except:
        goods_count += 1
        print(goods_count)

products = goods_list.find_elements_by_class_name("gallery-list-item")
products_list = []

for product in products:
    product_info = {}
    item = product.find_element_by_tag_name('a')
    product_link = item.get_attribute('href')
    product_name = item.get_attribute('data-track-label')
    price = product.find_element_by_class_name('c-pdp-price__current').text

    product_info['name'] = product_name
    product_info['price'] = price
    product_info['link'] = product_link
    products_list.append(product_info)

client = MongoClient('localhost', 27017)
db = client['mvideo_goods']
db.mvideo_goods.delete_many({})
db.mvideo_goods.insert_many(products_list)

driver.quit()
