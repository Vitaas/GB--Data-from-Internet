# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

class WebparserItem(scrapy.Item):

    _id = scrapy.Field()
    name = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()


class WebparserItemSJ(scrapy.Item):

    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
