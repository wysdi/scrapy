import scrapy
from ..items import ScrapperItem


class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['codepolitan.com', 'buildwithangga.com', 'dicoding.com']
    start_urls = [
        # 'https://buildwithangga.com/kelas',
        # 'https://www.dicoding.com/academies/list',
        'https://www.codepolitan.com/library#courses'
    ]

    def start_requests(self):
        for url in self.start_urls:
            if url == 'https://buildwithangga.com/kelas':
                yield scrapy.Request(url, callback=self.parse_bwa)
            elif url == 'https://www.dicoding.com/academies/list':
                yield scrapy.Request(url, callback=self.parse_dicoding)
            elif url == 'https://www.codepolitan.com/library#courses':
                yield scrapy.Request(url, callback=self.parse_codepolitan)

    def parse_bwa(self, response):
        for card in response.xpath('//div[has-class("card-body pb-0")]'):
            # Cleaned Field
            cleaned_title = card.xpath('./h6/text()').extract_first().strip()
            cleaned_link = card.xpath('./a[@class="stretched-link"]/@href').extract_first()
            cleaned_price = card.xpath('.//div[3]/div[1]/h6/text()').extract_first().strip()
            cleaned_type = card.xpath('.//span[2]/text()').extract_first()
            cleaned_rating = card.xpath('.//div[3]/div[2]/p/text()').extract_first()
            cleaned_img = card.xpath('.//img[@class="img img__cover"]/@src').extract_first()

            item = ScrapperItem()
            item['title'] = cleaned_title
            item['link'] = cleaned_link
            item['price'] = cleaned_price
            item['type'] = cleaned_type
            item['rating'] = cleaned_rating
            item['img'] = cleaned_img
            item['site'] = response.request.url.split('/')[2]

            yield item

    def parse_dicoding(self, response):
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


    def parse_codepolitan(self, response):
        # pass
        for card in response.xpath('//div[has-class("box-kelas text-lg-left text-xl-left container")]'):
            # Cleaned Field
            cleaned_title = card.xpath('.//h5/text()').extract_first().strip()
            # cleaned_link = card.xpath('./a[@class="remove-style-link"]/@href').extract_first()
            # cleaned_price = card.xpath('.//div[3]/div[1]/h6/text()').extract_first().strip()
            # cleaned_type = card.xpath('.//span[2]/text()').extract_first()
            # cleaned_rating = card.xpath('.//div[3]/div[2]/p/text()').extract_first()
            # cleaned_img = card.xpath('.//img[@class="lazy img-fluid"]/@src').extract_first()

            item = ScrapperItem()
            item['title'] = cleaned_title
            # item['link'] = cleaned_link
            item['site'] = response.request.url.split('/')[2]
            # item['price'] = cleaned_price
            # item['type'] = cleaned_type
            # item['rating'] = cleaned_rating
            # item['img'] = cleaned_img

            yield item

    
