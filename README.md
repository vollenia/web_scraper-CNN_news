# web_scraper-CNN_news

## Summary
The goal of this project is to collect data from the CNN (Cable News Network) website for a time specific window, store it in a database which can then be searched for specific contents.

To run the code call _scrapy crawl CNN_ from the terminal. When prompted, provide the full year then month (month without the leading 0 for single-digit months).
After the scraping process is finished the .xml database will be stored to the _databases_ directory and can be accessed directly or later by running _access.py_.
When accessing the database, select the database, one of the _tags_ that is to be searched and provide a keyword to be searched for.
Articles that meet the requirements will be printed in full (including the content of all the tags) to console while displaying the total number of articles found.

The scraping framework _Scrapy_ was used and the code was tested to run under Python 3.8.10. The python environment can be recreated by using the included _requirements.txt_.
This is all you need to know to scrape the CNN website and store/access the created databases.

## Data
--CNN (Cable News Network) webpage
(provides a listing of articles with the corresponding dates)
Listings range form August 2011 - Present day (DATE)

## Framework
Scrapy (what is scrapy)

## Modules Overview

The main steps of the project can be summarized as follows:
*Collect data from HTML
*Prepare data to be a database in XML format
*Access data within the XML databse by attributes

### 1. Collecting the Data (cnn_news.py)
The class CnnSpider incorporates input from the user to navigate the CNN website. It first uses the _CNN sitemap_ to extract the _date_, _title_ and _url_ of the articles within the selected time frame, then follows the _urls_ to the individual web pages to furter extract the _author_, _short summary of the text_ and the _full text_. This is achieved by parsing the HTML structure and identifying the tags that carry the information relevant for this task via css extractors.

In some cases the extracted data requires additional processing. Therefore, a data cleaning step is incorporated into the parsing process. Inconsistencies were especially observed for the author where the HTML-tags somtimes contained additional text, a url or missing the name alltogether.
For cases with additional text and url the content is reduced to the name of the author and for missing author names the placeholder _CNN_ is put in place.

### 2. Storing the Data (...)
Data is stored in _xml_ format. For each articel, the incdividual content groupas are enclosed withing corresponding tags (_data_, _title_, _url_, _short_text (summary)_, _full_text_).
(picture)
The resulting _xml_ database is named according to the query made during the collection process.

### 3. Acsessing the Data (acess.py)
The function _access_xml()_ which is responsible for accessing the data can be ether called internally from _cnn_news.py_ after finishing the scraping process or externally by running _python access.py_ from the terminal.
When called, the function will display all the databases within the database directory. Then the user will be prompted to select a database and the type of tag to be searched. Only one database and tag can be searched at a time. The search is performed by providing a keyword which is then matched with the contents of the specified tags within the database via xpath queries.
The matched articles are first collected and then printed in the terminal with contents from all the tags while also displaying the total number of relevant articles and the progression.
