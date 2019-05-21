from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import os

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
    text = ''

    is_running = True
    p = page

    # Tags to search for
    html_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li']

    found_tags = []
    # while there is more tags in 'page'
    while is_running:
        start_tag = p.find('<')
        end_tag = p.find('>')
        tag = p[start_tag+1:end_tag]
        close_tag = p.find('</'+tag+'>')

        if tag in html_tags:
            html = p[start_tag:close_tag+3+len(tag)]
            found_tags.append(html)

        p = p[end_tag+1:]
        if start_tag == -1:
            is_running = False

    text += make_md(found_tags)

    file.write(text)
    file.close()
    os.chdir('..')

def make_md(found_tags):
    text = ''

    for tag in found_tags:
        start_tag = tag.find('<')
        end_tag = tag.find('>')
        tag_type = tag[start_tag+1:end_tag]
        close_tag = tag.find('</'+tag_type+'>')
        content = tag[end_tag+1:close_tag]
        if content.find('<') == -1:
            # No more tags in content
            text += content + '\n'
        else:
            content = content.replace('<ul>','')
            content = content.replace('</ul>','')
            content = content.replace('<li>','*')
            content = content.replace('</li>','\n')
            text += content
        
    return text
