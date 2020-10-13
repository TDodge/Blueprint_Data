# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import datetime

class S1Pipeline(object):
	def __init__(self):
		self.create_connection()
		self.create_table()

	def create_connection(self):
		self.conn = sqlite3.connect('/Users/thomasdodge/Desktop/PythonProjects/BlueprintData/s1/edgar.sqlite')
		self.cur = self.conn.cursor()

	def create_table(self):
		self.cur.execute("""DROP TABLE IF EXISTS s1_forms_v2""")
		self.cur.execute("""CREATE TABLE s1_forms_v2(scraped_time text, page_link text, no_var text, doc_link text, form_type text, company_name text, company_link text, filing_date text)""")

	def process_item(self, item, spider):
		self.store_db(item)

	def store_db(self,item):
		self.cur.execute("""INSERT INTO s1_forms_v2 values (?,?,?,?,?,?,?,?)""", (datetime.datetime.now(), item['page_link'], item['no_var'][0], item['doc_link'][0], item['form_type'][0], item['company_name'][0], item['company_link'][0], item['filing_date'][0]))
		self.conn.commit()


