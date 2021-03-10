import scrapy

from scrapy.loader import ItemLoader

from ..items import GbkrsiItem
from itemloaders.processors import TakeFirst


class GbkrsiSpider(scrapy.Spider):
	name = 'gbkrsi'
	start_urls = ['https://www.gbkr.si/medijsko-sredisce']

	def parse(self, response):
		post_links = response.xpath('//div[@class="listed-content__single-item"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="main-button main-button--small main-button--secondary--bordered"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="article-title"]/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h2)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=GbkrsiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		return item.load_item()
