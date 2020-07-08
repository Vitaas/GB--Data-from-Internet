# Урок 4. Парсинг HTML. XPath
# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
#
# 2)Сложить все новости в БД

from lxml import html
import requests
from pprint import pprint
from datetime import datetime
import pandas as pd
import re
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_db']

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def request_to_lenta():

    link_lenta = 'https://lenta.ru/'
    response = requests.get(link_lenta, headers=header)
    dom = html.fromstring(response.text)

    news_lenta = []
    items = dom.xpath("//div[contains(@class, 'js-main__content')]//div[@class='span4']/div[@class='item']"

    for item in items:
        news = {}
        title = item.xpath(".//a/text()")
        link = item.xpath(".//a/@href")
        date = item.xpath(".//a/time/@datetime")
        source = link_lenta

        news['title'] = title[0]
        news['link'] = link[0]
        news['date'] = date[0]
        news['source'] = source

        news_lenta.append(news)
        add_news_to_db(news)

    return(news_lenta)

def request_to_yandex():
    link_yandex = 'https://yandex.ru/news/'
    response = requests.get(link_yandex, headers=header)
    dom = html.fromstring(response.text)

    news_yandex = []
    items = dom.xpath("//div[@class='stories-set stories-set_main_no stories-set_pos_1']//td")

    for item in items:
        news = {}
        title = item.xpath(".//h2/a/text()")
        link = item.xpath(".//h2/a/@href")
        date = item.xpath(".//div[@class='story__date']/text()")
        source = link_yandex

        news['title'] = title
        news['link'] = link
        news['date'] = date
        news['source'] = source

        news_yandex.append(news)
        add_news_to_db(news)

    return (news_yandex)


def request_to_mail():

    link_mail = 'https://news.mail.ru'
    response = requests.get(link_mail, headers=header)
    dom = html.fromstring(response.text)

    news_mail = []
    items = dom.xpath("//div[@class='block block_bg_primary block_separated_top link-hdr']//span//a")

    for item in items:
        news = {}
        title = item.xpath(".//span/text()")
        link = item.xpath(".//a/@href")
        source = link_mail

        response_news = requests.get(news['href'], headers=header)
        dom_news = html.fromstring(response_news.text)

        date = dom_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']/text()")[0])

        news['title'] = title
        news['link'] = link
        news['date'] = date
        news['source'] = source

        news_mail.append(news)
        add_news_to_db(news)

    return (news_mail)

def add_news_to_db(news):
    try:
        db.news.insert_one(news)
    except:
        pass
