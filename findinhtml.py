from urllib.request import urlopen
from urllib.error import HTTPError
import os
import re

# Finds all the a tags in the page and returns a list of urls from the tags
def find_link_in_a_tags(url):
    i = url[::-1].find('/')
    base_url = url[:len(url)-i]

    try:
        page = str(urlopen(url).read())
    except HTTPError as err:
        if err.code == 404:
            print('404 Page not found: ' + url)
        else:
            print('Could not get this url: ' + url)
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

    # Scrapes the content and creates a markdown file
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
    text = ''
    
    # Get headings
    headings = re.compile('<h.>(.*?)</h.>').search(page)
    for h in headings.groups():
        text += '#' + h
    
    text += '\n'
    p_tags = re.compile('<p.*?>(.*?)</p>').search(page)
    for p in p_tags.groups():
        if '<a' in p:
            text += '['+re.compile('<a.*?href="(.*?)".*?</a>').search(p).group(1)+']'
            text += re.compile('<a.*?>(.*?)</a>').search(p).group(1)

    #print(re.sub('<.*?>', '', page))
    file.write(text)
    file.close()
    os.chdir('..')