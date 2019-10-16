About the project

   The main idea of project is to make efficient fundamental data scraper which will provide accuratly sorted financial information.
   
   At the current state the scraper is a fully functioning and written using Scrapy library.
        The data is scrapped only from 2011 onwards.

   The main issue at the moment is improving the accuracy of sorting and parsing methods.  

Installation
   Install requirement.txt using pip
  
   To scrape data run scraper.py and pass symbols of companies you want to scrape.
    
        python scraper.py AAPL AMZN FB
   The scraped files are stored in scraped folder 

   To parse all scraped files just run parser.py
        Parsed files stored inside parsed folder and it also creates one single file for each statment inside All folder.

I am activly seeking contributers to improve effeciency, structure and functionality.

This project is licensed under the terms of the MIT license."# SEC-EDGAR-python-scraper" 
