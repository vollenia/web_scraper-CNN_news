"""
Access script:
Requires data files to already be downloaded.
Ideally run from directory where data files are located.
"""

from os import listdir
from os.path import isfile, join
from lxml import etree

def access_xml():
    # Show all files in current directory
    files_list = [f for f in listdir('databases') if isfile(join('databases', f))]
    #print(f'{files_list=}')
    print("Databases in current directory:")
    for file in files_list:
        if file.endswith('.xml'):
            print('\t' + file)

    # Request name of one data file
    filename = input("Which database would you like to search?: ")

    # Parse XML-tree
    tree = etree.parse(join('databases', filename))
    root = tree.getroot()

    # Request XPath-Query and use it to search in XML-tree
    tag = str(input("What category would you like to search (date, title, author, text)?: "))
    keyword = input("What keyword would you like to serch for?: ")
    query = "//*[contains(" + tag + ", '" + keyword + "')]"
    #print(f'{query=}')
    #query = input("Enter an XPath-query to search the database: ")
    result = root.xpath(query)
    #print(f'{result=}')
    
    # Print matched articles to console or error message
    if not result:
        print(f'No match in CATEGORY: "{tag}" for KEYWORD: "{keyword}"')
    else:
        for i, r in enumerate(result):
            if r is not None:
                print(f'\n---------- RESULT {i+1}/{len(result)} ----------')
                print('\nDATE: ', r.xpath('date')[0].text)
                print('\nTITLE: ', r.xpath('title')[0].text)
                print('\nAUTHOR: ', r.xpath('author')[0].text)
                print('\nTEXT_SHORT: ', r.xpath('textshort')[0].text)
                print('\nTEXT_FULL: ', r.xpath('textfull')[0].text)
                print('\nURL: ', r.xpath('url')[0].text)

if __name__ == "__main__":
    print(f'Accessing the xml externally...')
    access_xml()