# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class S1Item(scrapy.Item):
	no_var = scrapy.Field()
	doc_link = scrapy.Field()
	form_type = scrapy.Field()
	company_name = scrapy.Field()
	company_link = scrapy.Field()
	filing_date = scrapy.Field()
	page_link = scrapy.Field()

	
