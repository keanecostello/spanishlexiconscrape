# coding: utf-8


from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import pickle

base_url = 'https://www.spanishetym.com/directory/{}?page={}'
letters = [
    'a', 'b', 'c',
     'ch', 'd', 'e', 'f', 'g', 'h',
     'i', 'j', 'k', 'l', 'll', 'm', 'n', 'ñ', 'o',
     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
     'z'
]


def get_max_page(page_one_url, letter):
    # Get request and coerce to soup
    request = requests.get(page_one_url)
    soup = BeautifulSoup(request.content, 'html.parser')
    # Find all hrefs
    hrefs = [i['href'] for i in soup.findAll('a', href=True)]
    # if href is page number, store
    pages = []
    for i in hrefs:
        if i.startswith('/directory/{}?page='.format(letter)):
            pages.append(i)
    # for CH we need to use:
    if len(pages) == 0:
        return 1
    # return last page number
    return int(pages[-1].split('page=')[1])


def get_spanish_etym(row):
    # get first link in row, which is the word in question
    word = row.findAll('a', href=True)[0].getText()
    # get text for each section within row
    content_values = [i.getText() for i in row.findAll(lambda tag: tag.name == 'section')]
    # join text together and strip leading and trailing white space
    content = ' '.join(content_values).strip()
    # return word/content as dictionary 
    return {word: content}


def get_single_page_content(full_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'}

    for i in range(3):
        # Get request and coerce to Soup
        request = requests.get(full_url, headers=headers)
        soup = BeautifulSoup(request.content, 'html.parser')
        # Find table
        table = soup.find(lambda tag: tag.name == 'table')

        # Check table exists
        if table is None:
            # if not exists, sleep for a second and try again
            sleep(15)
        else:
            # if table exists keep going
            break

    # If table not exists after three attempts, print warning and skip
    if table is None:
        print("Failed to Find Table on Page - Some Data May Be Missing")
        return {}

    # Find all rows in table
    rows = table.findAll(lambda tag: tag.name == 'tr')

    # Get content for reach row
    all_etym = [get_spanish_etym(row) for row in rows]

    # Iterate through each set of content, add to dictionary and return
    results = {}
    [results.update(r) for r in all_etym]
    return results


def get_all_letter_content(letter):
    # Get max page for letter in question
    base_url = 'https://www.spanishetym.com/directory/{}?page={}'
    max_page = get_max_page(base_url.format(letter, 1), letter)
    print("Found {} Pages for Letter {}".format(max_page, letter))

    # initialize empty dictionary
    all_page_results = {}

    # For each page number
    for page_number in range(1, max_page + 1):
        print("\tGetting content for page {}".format(page_number))
        full_url = base_url.format(letter, page_number)
        # Get content for page
        all_page_results.update(get_single_page_content(full_url))
    return all_page_results


# In[12]:


all_letter_content = [get_all_letter_content(letter) for letter in letters]

csv_results = {}
[csv_results.update(r) for r in all_letter_content]
df = pd.DataFrame(data=[list(csv_results.keys()), list(csv_results.values())]).transpose()
df.to_csv("etym_scrape_results.csv")
