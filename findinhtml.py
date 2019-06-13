from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import re
import os

# Finds all the a tags in the page and returns a list of urls from the tags
def find_links_in_page(url):
    # Finds the last "/" by reversing the string and find the first occurence of "/"
    i = url[::-1].find('/')

    # Stores the first part of the url until the the last "/"
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
    
    # Find all the "a" tags
    more = True
    # Holds the current part of the page starting with the whole page
    p = page
    # Stores the links found in the page
    links = []
    # While there is still more text in the page
    while more:
        p2 = p
        start = p2.find('<a ')
        stop = p2.find('</a>')
        # Stores the whole "a" tag
        link = p2[start:stop+4]

        # Split the "a" tag by space
        splitted = link.split(' ')
        # For each item in splitted
        for s in splitted:
            if 'href="' in s:
                first = s.find('href="')
                #Gets second occurence of "
                last = s.find('"', s.find('"')+1)
                # Store the link found i the "href" attribute
                l = s[first+6:last]
                # Add the link to the links list
                links.append(l)
        # If end tag not found, set more equals false
        if stop == -1:
            more = False
        # Set p variable equal next part of page
        else:
            p = p2[stop+4:]

    # Scrape the content and create a markdown file
    scrape_content(page, url)

    urls = []
    # Find all links and add base url if not already there.
    for l in links:
        if 'http' not in l:
            urls.append(base_url + l)
    return urls

# Creates a markdown file from the url name based on url
def scrape_content(page, url):
    # Change directory to the scrapes folder
    os.chdir('scrapes')
    # Create filename from url
    file_name = url.replace('/','_')+'.md'
    # Create file with above filename
    file = open(file_name, 'w+')

    # Join whole page to one line by splitting page by whitespace
    page = " ".join(page.split())

    text = ''

    # Defines wich html tags is relevant
    validate = '<h1>.*?</h1>|<h2>.*?</h2>|<h3>.*?</h3>|<h4>.*?</h4>|<h5>.*?</h5>|<h6>.*?</h6>|<p>.*?</p>|<ul>.*?</ul>|<li>.*?</li>'
    # Create list with all tags defined above
    relevant_tags = re.findall(validate, page)

    # For each tag convert to markdown and add to the text variable
    text = " ".join([make_markdown(tag) for tag in relevant_tags])

    #for tag in relevant_tags:
    #    text += make_markdown(tag)

    file.write(text)
    file.close()
    os.chdir('..')

# Converts html to markdown syntax
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
        md = md.replace('</ul>', '')
    if '<li>' in md:
        md = md.replace('<li>', '\n* ')
        md = md.replace('</li>', '')
        md = md.replace('<li> ', '\n* ')
    

    # Convert all a tags inside tags
    more_links = True
    while more_links:
        if '<a' in md:
            start = md.find('<a')
            end_start = md.find('>')
            end_tag = md.find('</a>')

            whole_tag = md[start:end_tag+4]
            start_tag = md[start:end_start+1]
            clickable_link = md[end_start+1:end_tag]

            href_start = start_tag.find('href="')+6
            href_to_end = start_tag[href_start:]
            href_end = href_to_end.find('"')
            href = start_tag[href_start:href_start+href_end]
            
            md = md.replace(whole_tag, '['+clickable_link+']('+href+')')
        else:
            more_links = False
            
    return md