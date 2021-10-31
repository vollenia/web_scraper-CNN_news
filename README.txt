Collect & Prepare:

Requires installed scrapy
Name of Spider: "CNN"
To start, simply use scrapy crawl, eg.:


scrapy crawl CNN -o example.xml --nolog (to supress the console output)
[UPDATE1: scrapy crawl CNN -O example.xml --is sufficient since settings were set to LOG_ENABLED = False]
-if run repeatedly the output will be appended to example.xml
-to override the contents of exmaple.xml use: -O instead -o
[UPDATE2: scrapy crawl CNN


Enter year between 2011 and 2020.
Enter month *without* leading 0.






Access:

Start access.py, indeally from the folder where xml files are stored.
Files should be listed, otherwise enter full path to xml file.
Enter any XPath Query, e.g.

//*[date='2020-01-18']
//*[contains(title, 'nurse')]