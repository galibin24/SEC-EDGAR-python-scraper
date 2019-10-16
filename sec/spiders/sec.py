
import scrapy

from scrapy.utils.project import get_project_settings

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
import bs4 as bs

from scrapy.selector import Selector
import pandas as pd 
import re, requests

import urllib.request

class MainSpider(CrawlSpider):
    name = 'sec'

    def __init__(self, company='',start_url = '' ,*args, **kwargs): 
        super(MainSpider, self).__init__(*args, **kwargs) 
        self.start_urls = start_url
        self.company = company
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback= self.parse_item, dont_filter=True)

    # pass links to main archive not Cik values
    def parse_item(self, response):
        data = response.text
        soup = bs.BeautifulSoup(data, features= 'lxml')
        links = []
        dates = []

        for link in soup.select('#main-content table tr td a '):
            i = 'https://www.sec.gov' + link.get('href')
            links.append(i)

        for date in soup.select('#main-content table tr td:nth-of-type(3)'):
            d = date.get_text()[0:10]
            if int(d[0:4]) >= 2010:
                dates.append(d)
            
        length = (len(dates))
        dictionary = dict(zip(links[0:length], dates))
         
        for key, value in dictionary.items():
            yield scrapy.Request(key, callback = self.parse_item1, meta={'date': value, 'link' : key})

    def parse_item1(self, response):
        date = response.meta['date']
        data = response.xpath('//td//a/@href').getall() 
        company = response.meta['link']
        company = company.split('/')[-2]

        R = ['R' + str(i) + '.htm' for i in range(2,10) ]

        Reports_links = []
        Rs = []
        for i in R:
            for d in data:
                if i in d :      
                    link = 'https://www.sec.gov' + d
                    Rs.append(i[0:2])
                    Reports_links.append(link)

        dictionary = dict(zip(Reports_links, Rs))

        if Reports_links:
            for key, value in dictionary.items():
                yield scrapy.Request(key, callback = self.main_parse, meta={'date': date, 'R': value, 'company' : company})

    def main_parse(self, response):
        date = response.meta['date']
        R = response.meta['R']
        company = response.meta['company']
        source = response.text  
        soup = bs.BeautifulSoup(source,'lxml')
        # find a table 
        table = soup.table
        table = soup.find('table')
        table_rows = table.find_all('tr')

        # parse for rows 
        clear  = []
        for tr in table_rows:
            try:
                td = tr.find_all('td')
                row = [i.text for i in td]
                clear.append(row)
            except:
                continue
        # put rows in dataframe and save
        df = pd.DataFrame(clear)
        name = company + ' ' + date + R + '.csv'
        name = name.replace('/', '')
        name = './files/' + name 
        df.to_csv(name)
