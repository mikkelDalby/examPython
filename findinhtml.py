from urllib.request import urlopen
from urllib.error import HTTPError
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

    is_running = True
    p = page

    html_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li']
    while is_running:
        start_tag = p.find('<')
        end_tag = p.find('>')
        tag = p[start_tag+1:end_tag]

        close_tag = p.find('</'+tag+'>')

        if tag in html_tags:
            if tag in html_tags[0]:
                text += '# ' + p[end_tag+1:close_tag]
            elif tag in html_tags[1]:
                text += '## ' + p[end_tag+1:close_tag]
            elif tag in html_tags[2]:
                text += '### ' + p[end_tag+1:close_tag]
            elif tag in html_tags[3]:
                text += '#### ' + p[end_tag+1:close_tag]
            elif tag in html_tags[4]:
                text += '##### ' + p[end_tag+1:close_tag]
            elif tag in html_tags[5]:
                text += '###### ' + p[end_tag+1:close_tag]
            elif tag in html_tags[6]:
                t = p[end_tag+1:close_tag]
                more_tags = True
                i = 0
                while more_tags:
                    start_nested = t[i:].find('<')
                    end_nested = t[i:].find('>')
                    nested_tag = t[i:][start_nested+1:end_nested]
                    if not start_nested == -1:
                        if 'a' in nested_tag[0]:
                            nested_close_tag = t.find('</a>')
                            clickable_link = t[end_nested+1:nested_close_tag]
                            t.replace(clickable_link, '['+clickable_link+']')
                            href = t.find('href="')+6
                            href_end = t.find('"', t.find('"')+1)
                            t.replace(t[start_nested:end_nested+1], t[href:href_end])
                            print(t[href:href_end])
                            i = nested_close_tag+4
                    else:
                        more_tags = False
                        
                text += t
            if tag in html_tags[7]:
                text += p[end_tag+1:close_tag]
            if tag in html_tags[8]:
                text += p[end_tag+1:close_tag]
            if tag in html_tags[9]:
                text += p[end_tag+1:close_tag]
            text += '\n'
        
        p = p[end_tag+1:]
        if start_tag == -1:
            is_running = False

    file.write(text)
    file.close()
    os.chdir('..')