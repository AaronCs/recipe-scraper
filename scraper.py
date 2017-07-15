from lxml import html
from queue import Queue
import threading
import requests
import logging

# Scrapes recipes off of allrecipes.com
# TODO: Figure out how many pages of recipes there are.
# Should I actually do this? I could optionally just check for the 404 page itself.


# Is this actually necessary?
class Recipe:
    def __init__(self, name='', description='', ingredients=[], directions=[]):
        # No need for overloading because of default arguments.
        # Possibly add source and the author?
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.directions = directions

    # TODO: Possible 'write' method to save it? Probably keep it outside the class.


def get_links(max_page):
    # Save links in something, text file?
    # Have a separate thing grab the recipe.
    for i in range(5):
        page_link = 'http://allrecipes.com/recipes/?page={0}#{0}'.format(i)
        print(page_link)
    page = requests.get(page_link, timeout=5)
    tree = html.fromstring(page.content)
    categories = tree.xpath("//a[@class='hero-link__item']/span/text()")
    links = tree.xpath("//a[@class='hero-link__item']/@href")
    '''
    new_page = requests.get(links[0])
    new_tree = html.fromstring(new_page.content)
    test = new_tree.xpath('//a')
    for items in links:
        logging.info('Link: %s', items)
    '''

# def parse_recipe(link):
    # Grabs a recipe from the queue.
    # Parse the recipe from the passed in arg, store in an object.
    # Should the arg be a link or the html itself?

# def populate_queue(page):
    # Populates the queue with recipe links, starting from the page in the arg.


def main():
    # get_links()
    get_links(5)

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    main()
    #print('done')
