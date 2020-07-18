import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&fromSearch=true&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()

        vacansy_links = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)

        yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()
        salary_min = response.css('div.vacancy-title meta[itemprop="minValue"]::attr(content)').extract()
        salary_max = response.css('div.vacancy-title meta[itemprop="maxValue"]::attr(content)').extract()
        url = response.css('div.bloko-column_xs-4 div[itemscope="itemscope"] meta[itemprop="url"]::attr(content)').extract()

        yield JobparserItem(name=name, salary=salary, salary_min=salary_min, salary_max=salary_max, url=url, site=self.start_urls[0])
