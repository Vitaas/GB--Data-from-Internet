import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css(
            'div._1ID8B div.f-test-vacancy-item div._3wZVt a._3dPok::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('div._3MVeX h1._3mfro::text').extract_first()
        salary = response.css('div._3MVeX span._2Wp8I span::text').extract()

        yield JobparserItem(name=name, salary=salary, url=response.url, site=self.start_urls[0])