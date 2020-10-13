import scrapy
from s1.items import S1Item
from time import sleep
from random import uniform

class s1(scrapy.Spider):
	name = 's1'

	start_urls = ['https://sec.report/Document/Header/?formType=S-1']

	def parse(self, response):

		items = S1Item()

		all_rows = response.css('table, tbody, tr')

		for row in all_rows:
			if row.css('th::text').extract_first()!= "No":
				items['page_link'] = response.url
				items['no_var'] = row.css('td:nth-child(1)::text').extract()
				items['doc_link'] = row.css('td:nth-child(2) a::attr(href)').extract()
				items['form_type'] = row.css('td:nth-child(3)::text').extract()
				items['company_name'] = row.css('td:nth-child(4) a::text').extract()
				items['company_link'] = row.css('td:nth-child(4) a::attr(href)').extract()
				items['filing_date'] = row.css('td:nth-child(5)::text').extract()

				yield items

		all_pages = response.css('a[rel="nofollow"][href*="Document"]::attr(href)').extract()

		for page in all_pages:
			next_page = 'https://sec.report'+str(page)
			yield response.follow(next_page, callback=self.parse)


