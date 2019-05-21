from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import re
import os

# Finds all the a tags in the page and returns a list of urls from the tags
def find_link_in_a_tags(url):
    i = url[::-1].find('/')
    base_url = url[:len(url)-i]

    try:
        page = urlopen(url).read()
        page = str(page.decode('utf-8'))
    except HTTPError as err:
        if err.code == 404:
            print('404 Page not found: ' + url)
        else:
            print('Could not get this url: ' + url)
        return []
    except URLError as err:
        print('Check your internet connection')
        return []
    
    i = 0
    p = page
    links = []
    while i != -1:
        p2 = p[i:]
        start = p2.find('<a ')
        stop = p2.find('</a>')
        link = p2[start:stop+4]

        splitted = link.split(' ')
        for s in splitted:
            if 'href="' in s:
                first = s.find('href="')
                #Gets second occurence of "
                last = s.find('"', s.find('"')+1)
                l = s[first+6:last]
                links.append(l)
        if stop == -1:
            i = -1
        else:
            p = p2[stop+4:]

    # Scrape the content and create a markdown file
    scrape_content(page, url)

    urls = []
    for l in links:
        if 'http' not in l:
            urls.append(base_url + l)
    return urls

def scrape_content(page, url):
    os.chdir('scrapes')
    file_name = url.replace('/','_')+'.md'
    file = open(file_name, 'w+')

    page = page.strip(' ')
    
    page = page.replace('<h1>','# ')
    page = page.replace('</h1>','\n')
    page = page.replace('<h2>','## ')
    page = page.replace('</h2>','\n')
    page = page.replace('<h3>','### ')
    page = page.replace('</h3>','\n')
    page = page.replace('<h4>','#### ')
    page = page.replace('</h4>','\n')
    page = page.replace('<h5>','##### ')
    page = page.replace('</h5>','\n')
    page = page.replace('<h6>','###### ')
    page = page.replace('</h6>','\n')
    page = re.sub('<p.*?>', '', page)
    page = page.replace('</p>', '\n')
    page = re.sub('<ul.*?>', '', page)
    page = re.sub('</ul.*?>', '\n', page)
    page = re.sub('<li.*?>', '*', page)
    page = re.sub('</li.*?>', '', page)

    file.write(page)
    file.close()
    os.chdir('..')