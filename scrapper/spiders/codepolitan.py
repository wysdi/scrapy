import scrapy


class CodepolitanSpider(scrapy.Spider):
    name = 'codepolitan'
    allowed_domains = ['codepolitan.com']
    start_urls = ['http://codepolitan.com/']

    def parse(self, response):
        pass
