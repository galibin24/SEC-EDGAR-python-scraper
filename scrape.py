#!/usr/bin/env python

import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy 
import re, requests
import bs4 as bs
import urllib.request
from sys import argv
import pandas as pd
import random
import os


# TODO before starting extensive scraping jobs implement a solid proxy system(Late stage dev)

tickers = input("Enter Tickers: ").split() 
year  = int(input("Enter from which year to start: "))

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
    return cik_dict

# reads files names in files directory
def raw_files():
    files = []
    for file in os.listdir("./files"):
        if file.endswith(".csv"):
            pat = os.path.join("./files", file)
            files.append(pat)
    return files


# check if provided Tickers already have CIKs and return URL 
def look_up(Tickers):
    # read existing tickers
    existing_df = pd.read_excel('Sorted.xlsx', index_col = 0)
    ex_Tickers = existing_df['Ticker'].values.tolist()
    # compare existing tickers and add non existing tickers
    for t in Tickers:
        if t in ex_Tickers:
            print(t + ' already exists')
        else:
            print(t + " doesn't exist")
            links = getCIK([t])
            new_part = pd.DataFrame(list(links.items()), columns = ['Ticker', 'CIK'])
            existing_df = existing_df.append(new_part, ignore_index = True)
    existing_df.to_excel('Sorted.xlsx')
    
    URLs = []
    # get names of already scraped CIKs
    names = [i.split(' ')[0] for i in raw_files() ] 
    names = [i.split('\\')[-1] for i in names ]
    # get CIKs for required tickers and convert to URL
    for t in Tickers:
        df = existing_df.loc[existing_df['Ticker'] == t]     
        CIK = str(df['CIK'].values[0])
        # Check if company data already has been scraped 
        if CIK in names:
            print(CIK + 'already scraped')
        else:
            URL = 'https://www.sec.gov/Archives/edgar/data/' + CIK
            URLs.append(URL)
    return URLs


# Start Spider provided the links  
process = CrawlerProcess(get_project_settings())        

def scrape(links, year):
    for i in links:
        process.crawl('sec', start_url=links, company = i, year = year)
        process.start()

scrape(links = look_up(Tickers = tickers ), year = year)
