import scrapy
from ..items import ScrapperItem


class DicodingSpider(scrapy.Spider):
    name = 'dicoding'
    allowed_domains = ['dicoding.com']
    start_urls = ['https://www.dicoding.com/academies/list']

    def parse(self, response):
        for card in response.xpath('//div[has-class("cta-to-detail")]'):
            # Cleaned Field
            cleaned_title = card.xpath('.//a[@class="remove-style-link"]/p/text()').extract_first().strip()
            cleaned_link = card.xpath('./a[@class="remove-style-link"]/@href').extract_first()
            # cleaned_price = card.xpath('.//div[3]/div[1]/h6/text()').extract_first().strip()
            # cleaned_type = card.xpath('.//span[2]/text()').extract_first()
            # cleaned_rating = card.xpath('.//div[3]/div[2]/p/text()').extract_first()
            # cleaned_img = card.xpath('.//img[@class="lazy img-fluid"]/@src').extract_first()

            item = ScrapperItem()
            item['title'] = cleaned_title
            item['link'] = cleaned_link
            item['site'] = response.request.url.split('/')[2]
            # item['price'] = cleaned_price
            # item['type'] = cleaned_type
            # item['rating'] = cleaned_rating
            # item['img'] = cleaned_img

            yield item
