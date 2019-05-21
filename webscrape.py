from findinhtml import *
import sys

visited = set()
#url = 'https://clbokea.github.io/exam/'

def main():
    # If no url is provided this will be used
    default_url = 'https://clbokea.github.io/exam/'
    try:
        url = sys.argv[1]
    except IndexError as err:
        print('No url provided... Using default url: ' + default_url)
        url = default_url
    # Find all links in index url
    links = find_link_in_a_tags(url)

    # While there is still links to follow
    while len(links) != 0:
        cur_link = links[0]
        if cur_link not in visited:
            print('Scraping: ' + cur_link)
            n_links = find_link_in_a_tags(cur_link)
            for l in n_links:
                if l not in links:
                    links.append(l)
            visited.add(cur_link)
            
        links.remove(cur_link)

if __name__ == "__main__":
    main()