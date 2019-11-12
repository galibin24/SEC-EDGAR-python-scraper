# About this project 

   The main idea of project is to make efficient fundamental data scraper which will provide accurately sorted financial information.
   
   At the current state the scraper is a fully functioning and written using Scrapy library.
        The data is scrapped only from 2011 onward.

   The labeling script decides on the document type and stores it in parsed folder.

   The Aggregation script is in very raw stage of progress and I will be working on it in the upcoming month.  

## Getting Started
   Copy the repository and Install requirement.txt using pip
  
   To scrape data run scraper.py and pass symbols of companies you want to scrape and year.
        python scraper.py
        
   The scraped files are stored in scraped folder 

   To label all scraped files just run 
      ```
         label.py
      ```.

## Contribution
I am actively seeking contributors to improve efficiency, structure and functionality.

## License

This project is licensed under the terms of the MIT license.

"# SEC-EDGAR-python-scraper" 

## A note 
Also, I am third year finance major, and been learning programming for less than a year, therefore the code inefficiencies and the structure might look out of place as I am not familiar with many programming convensions. 
