# About this project 

   The main idea of project is to make efficient fundamental data scraper which will provide accurately sorted financial information.
   
   At the current state the scraper is a fully functioning and written using Scrapy library.
        The data is scrapped only from 2011 onward.

   The main issue at the moment is improving the accuracy of sorting and parsing methods.  

## Getting Started
   Copy the repository and Install requirement.txt using conda(recomended) or pip.
  
   To scrape data run scraper.py and pass symbols of companies you want to scrape.
    
        python scraper.py AAPL AMZN FB
        
   The scraped files are stored in scraped folder 

   To parse all scraped files just run 
      ```
         parser.py
      ```.
   Parsed files stored inside parsed folder and it also creates one single file for each statement inside All folder.


## Contribution
I am actively seeking contributors to improve efficiency, structure and functionality.

## A note 
Also, I am third year finance major, and been learning programming for less than a year, therefore the code inefficiencies and the structure might look out of place as I am not familiar with many programming convensions. 

## License

This project is licensed under the terms of the MIT license.

"# SEC-EDGAR-python-scraper" 
