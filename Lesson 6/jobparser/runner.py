from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from providerparser import settings
from providerparser.spiders.tripru import TripruSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(TripruSpider)

    process.start()
