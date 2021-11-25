# Scrapy spider
# Contains required logic to find all articles from a given month and extract relevant data fields.

import scrapy
from scrapy import signals
from ..items import CnnItem
import functools
from access import access_xml

# Requesting the year/month to collect the data
year = input("Enter the YEAR you want to retrieve: ")
month = input("Enter the MONTH you want to retrieve: ")

# Spider class
class CnnSpider(scrapy.Spider):
    name = "CNN"
    start_urls = ["https://edition.cnn.com/article/sitemap-"+str(year)+"-"+str(month)+".html"]

    custom_settings = {
        "FEED_URI": "databases/CNN_" + year + "_" + month + ".xml",
        "FEED_FORMAT": "xml"
        }
    
    # Initiating singnals for starting and finishing the scraping process
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CnnSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        print("1/4: Opened {} spider".format(spider.name))
        print("2/4: Running...")

    # Calling access.py uppon finishig the scraping process (if desired by the user) 
    def spider_closed(self, spider):
        print("3/4: Closed {} spider".format(spider.name))
        access = str(input("4/4: Do you want to search the scraped data (y/n)?: "))
        if access == "y":
            print("Accessing the xml internally...")
            access_xml()

    # Parse the sitemap - view of the given month
    def parse(self, response):
        
        # Get all articles
        all_entries = response.css("div.sitemap-entry ul li")
        for entry in all_entries:
            
            # Set up an item for each article and fill with data from sitemap-view
            item = CnnItem()
            date = entry.css("span.date::text").extract_first()
            title = entry.css("span.sitemap-link a::text").extract_first()
            url = entry.css("span.sitemap-link a::attr(href)").get()

            # Assign data to item-fields
            item["date"] = date
            item["title"] = title
            item["url"] = url

            # Generate new request from the assigned URL, callback to second parse function and pass along item
            callback = functools.partial(self.parse_next, item)
            yield scrapy.http.Request(url, callback=callback)


    # Parse "second" request from a URL: the actual article page of an article; takes item as input from sitemap-view
    def parse_next(self, item, response):

        # Extract information from article page
        #Author
        author = response.css(".metadata__byline__author::text, .metadata__byline__author a::text").extract()
        author = "".join(author) # joining multiple values if there are any (e.g. text + href name)
        author = author.strip().strip(',')
        # Set "author" to "CNN" if author is missing
        if author == "" or author.lower() == "by": # older articles are missing the author (e.g. "By ")
            author = "CNN"
        # In cases where [author] is present, remove "By" (e.g. "By [author name]" --> "[author name]")
        # Cases with "CNN's [author]" have been left unprocessed since it represents a collaboration between CNN and other sources
        if author.lower()[:3] == "by ":
            author = author[3:]
        elif author.lower()[:9] == "story by ":
            author = author[9:]
        elif author.lower()[:12] == "analysis by ":
            author = author[12:]
        elif author.lower()[:5] == "from ":
            author = author[5:]
        item["author"] = author

        # Short text
        textshort = response.css(".speakable::text, .speakable a::text").extract()
        item["textshort"] = "".join(textshort)

        # Full text
        textfull = response.css(".zn-body__paragraph::text, #body-text a::text").extract()
        item["textfull"] = "".join(textfull)

        # Final item is yielded, scrapy will store this in output file if specified by command-line
        yield item