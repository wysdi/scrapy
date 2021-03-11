import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ..items import ScrapperItem


class CodepolitanSpider(scrapy.Spider):
    name = 'codepolitan'
    allowed_domains = ['codepolitan.com']
    start_urls = ['https://www.codepolitan.com/library#course']

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapper.pipelines.FirestorePipeline': 300,
        },
        'FEED_URI': './json/codepolitan.json'
    }
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=EC.element_to_be_clickable((By.XPATH, '//*[@id="courses"]/div[2]'))
            )

    def parse(self, response):
        driver = response.request.meta['driver']

        cards = response.selector.xpath('//*[@id="courses"]/div[1]/div/div')
        for card in cards:
            cleaned_title = card.xpath('.//h5/text()').extract_first().strip()
            cleaned_link = card.xpath('./a/@href').extract_first()
            cleaned_price = card.xpath('.//p[@class="mb-0 text-price font-weight-bold price-color"]/text()').extract_first()
            # cleaned_type = card.xpath('.//span[2]/text()').extract_first()
            # cleaned_rating = card.xpath('.//div[3]/div[2]/p/text()').extract_first()
            cleaned_img = card.xpath('.//img[@class="card-img-top mb-0 kelasImage"]/@src').extract_first()
            item = ScrapperItem()
            item['title'] = cleaned_title
            item['link'] = response.request.url.split('/')[2] + cleaned_link
            item['price'] = cleaned_price
            item['img'] = cleaned_img
            item['site'] = response.request.url.split('/')[2]

            yield item

            button_next = driver.find_element_by_xpath("//button[contains(text(), 'Next')]")
            if button_next.is_enabled():
                button_next.click()

