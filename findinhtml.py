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
            
    i = 0
    p = page
    links = []
    while i != -1:
        p2 = p[i:]
        start = p2.find('<')
        stop = p2.find('</')
        start_tag = p2[start+1:start+3]
        stop_tag = p2[stop+2:stop+4]

        search_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p ', 'p>', 'a ', 'em']

        is_in_p = False

        if not '/' in start_tag[0]:
            if start_tag in search_tags:
                t = p2[start:stop]
                e = t.find('>')+1
                line = t[e:]
                if start_tag in search_tags[0]:
                    text += '# ' + line + '\n'
                if start_tag in search_tags[1]:
                    text += '## ' + line + '\n'
                if start_tag in search_tags[2]:
                    text += '### ' + line + '\n'
                if start_tag in search_tags[3]:
                    text += '#### ' + line + '\n'
                if start_tag in search_tags[4]:
                    text += '##### ' + line + '\n'
                if start_tag in search_tags[5]:
                    text += '###### ' + line + '\n'
                if start_tag in search_tags[6] or start_tag in search_tags[7]:
                    if not '<' in line:
                        text += line + '\n'
                    else:
                        # format links in paragrafs
                        a_start = line.find('<a')
                        temp_line = line[a_start:]

                        href_start = temp_line.find('href="')+6
                        href_line = temp_line[href_start:]
                        href_end = href_line.find('"')
                        link = href_line[:href_end]
                        
                        click_start = temp_line.find('>')+1
                        clickable_text = temp_line[click_start:]
                        
                        text += '['+clickable_text+']('+link+')'
                        
        
        if stop == -1:
            i = -1
        else:
            p = p2[start+4:]

    #print(re.sub('<.*?>', '', page))
    file.write(text)
    file.close()
    os.chdir('..')