#!/usr/bin/env python

import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy 
import re, requests
import bs4 as bs
import urllib.request
from sys import argv

process = CrawlerProcess(get_project_settings())

# Function to convert Tickers to CIK numbers
def getCIK(TICKERS):
    URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    CIK_RE = re.compile(r'.*CIK=(\d{10}).*')    
    cik_dict = {}
    for ticker in TICKERS:
        f = requests.get(URL.format(ticker), stream = True)
        results = CIK_RE.findall(f.text)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            cik_dict[str(ticker).upper()] = str(results[0])
    
    val = cik_dict.values()
    URLs = []
    for i in val: 
        # print(i)
        URL = 'https://www.sec.gov/Archives/edgar/data/' + i
        URLs.append(URL)

    return URLs

Tikcers = argv[1:]
links = getCIK(Tikcers)

def runspider(link, company):
    print(company)
    process.crawl('sec', start_url=link, company = company)    

# start loop to 
def scrape(Tickers = Tikcers):
    links = getCIK(Tickers)
    for i in Tickers:
        links = getCIK(Tickers)
        runspider(links, i)
        process.start()
        process.stop()

scrape(Tikcers)