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
    
    # Find all links in index url and store in "links"
    # Stores all links that needs to be visited
    links = find_links_in_page(url)

    # While there is still links to follow
    while len(links) != 0:
        # Grab the firts item in the list
        cur_link = links[0]
        if cur_link not in visited:
            print('Scraping: ' + cur_link)
            n_links = find_links_in_page(cur_link)
            # For each link in n_links add them to the "links" list
            for l in n_links:
                if l not in links:
                    links.append(l)

            # When all links are found and the page are scraped add to visited list
            visited.add(cur_link)

        # If page already visited remove from "links" list
        links.remove(cur_link)

def add_one(i):
    return i+1

def test_method():
    list = [1,2,3,4,5,6,7,8,9]
    l = [add_one(n) for n in list]
    print(l)



if __name__ == "__main__":
    main()