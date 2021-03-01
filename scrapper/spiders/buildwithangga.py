import scrapy
from ..items import ScrapperItem


class BuildwithanggaSpider(scrapy.Spider):
    name = 'buildwithangga'
    allowed_domains = ['buildwithangga.com']
    start_urls = ['https://buildwithangga.com/kelas']

    def parse(self, response):
        for card in response.xpath('//div[has-class("card-body pb-0")]'):
            # Cleaned Field
            cleaned_title = card.xpath('./h6/text()').extract_first().strip()
            cleaned_link = card.xpath('./a[@class="stretched-link"]/@href').extract_first()
            cleaned_price = card.xpath('.//div[3]/div[1]/h6/text()').extract_first()
            cleaned_type = card.xpath('.//span[2]/text()').extract_first()
            cleaned_rating = card.xpath('.//div[3]/div[2]/p/text()').extract_first()
            cleaned_img = card.xpath('.//img[@class="img img__cover"]/@src').extract_first()

            item = ScrapperItem()
            item['title'] = cleaned_title
            item['link'] = cleaned_link
            if cleaned_price:
                item['price'] = cleaned_price.strip()
            item['type'] = cleaned_type
            item['rating'] = cleaned_rating
            item['img'] = cleaned_img
            item['site'] = response.request.url.split('/')[2]

            yield item
