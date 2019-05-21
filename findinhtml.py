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

    page = " ".join(page.split())
    start = page.find('<h1>')+4
    end = page.find('</h1>')

    text = ''

    validate = '<h1>.*?</h1>|<h2>.*?</h2>|<h3>.*?</h3>|<h4>.*?</h4>|<h5>.*?</h5>|<h6>.*?</h6>|<p>.*?</p>|<ul>.*?</ul>|<li>.*?</li>'
    relevant_tags = re.findall(validate, page)
    for tag in relevant_tags:
        more_tags = re.findall(validate, tag)

        text += make_markdown(tag)

    file.write(text)
    file.close()
    os.chdir('..')

def make_markdown(tag):
    t = tag[1:3]
    md = tag
    if 'h1' in t:
        md = md.replace('<h1>','# ')
        md = md.replace('</h1>','\n')
    if 'h2' in t:
        md = md.replace('<h2>','## ')
        md = md.replace('</h2>','\n')
    if 'p' in t:
        md = md.replace('<p>', '')
        md = md.replace('</p>', '\n')
    
    if '<ul>' in md:
        md = md.replace('<ul>', '')
        md = md.replace('</ul>', '\n')
    if '<li>' in md:
        md = md.replace('<li>', '\n*')
        md = md.replace('</li>', '')
    
    
    return md