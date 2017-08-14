from lxml import html
from multiprocessing import Pool
import requests
import logging
import json
import time
from fake_useragent import UserAgent

# Scrapes recipes off of allrecipes.com
# TODO: Links grabber should only fire in certain cases to reduce runtime.

# ------ Recipe Link functions ------


def get_links(page_num):
    # Grabs all links on a page, and then appends it to a list.
    # The list will later be written into a file.
    page_link = 'http://allrecipes.com/recipes/?page={0}#{0}'.format(page_num)
    page = requests.get(page_link, timeout=5)
    tree = html.fromstring(page.content)
    links = tree.xpath("//article[@class='grid-col--fixed-tiles']/a/@href")

    return links


def write_recipe_links(recipe_array):
    # Write to a file.
    opened_file = open("recipe_links.txt", "w", encoding="utf-8")
    with opened_file as file:
        for link in recipe_array:
            file.write(link)
            file.write('\n')  # Newline as the delimiter.


def grab_links(num_links):
    # Wrapper function for writing recipe links.
    # link_array = []
    pool = Pool(5)

    with pool as pool:
            links = pool.map(get_links, range(num_links)) # Returns an array of an array.
            link_array = [link for subarray in links for link in subarray]
            # ^ Unpacks the links array of arrays into a flat array.
    link_array = list(set(link_array))  # Remove duplicates. Seems like a hack.
    write_recipe_links(link_array)  # Saves the links.

# ------ Recipe functions ------


def load_recipe_links(recipe_links):
    # Loads recipes into the array.
    opened_file = open("recipe_links.txt", "r", encoding="utf-8")
    with opened_file as file:
        for link in file:
            recipe_links.append(link)


def parse_recipe(link):
    # Parses the recipe ingredients and steps.
    to_parse = 'http://allrecipes.com{0}'.format(link).rstrip()  # rstrip removes the newline.
    page = requests.get(to_parse, timeout=5)
    tree = html.fromstring(page.content)
    title = tree.xpath("//h1[@class='recipe-summary__h1']/text()")
    ingredients = tree.xpath("//span[@itemprop='ingredients']/text()")
    directions = tree.xpath("//span[@class='recipe-directions__list--item']/text()")
    # Store results in a dictionary.
    # recipe_dict[title[0]] = {'ingredients': ingredients, 'directions': directions}
    if not title:
        raise ValueError("No title? Link: https://allrecipes.com" + link)
    return [title[0], ingredients, directions]


def write_recipe_info(recipe):
    # Saves recipe info into a json file.
    # Recipe is a dictionary (object, json)
    opened_file = open("recipes.json", "w", encoding="utf-8")
    with opened_file as file:
        json.dump(recipe, file)


def grab_all_recipes():
    # Wrapper function for writing recipes.
    # recipe_queue = Queue()  # It's faster with queues for some reason.
    recipe_links = []
    recipe_dict = {}
    pool = Pool(10)

    load_recipe_links(recipe_links)
    with pool as pool:
        # for link in recipe_links:
        recipes = pool.map(parse_recipe, recipe_links)  # WOOO I DID IT! IT MULTIPROCESSES STUFF!
        for recipe in recipes:
            recipe_dict[recipe[0]] = {'ingredients': recipe[1], 'directions': recipe[2]}
            # I could probably speed it up somehow by doing this a different way?
        # recipe = parse_recipe(link)  # Figure out how to multiprocess this. HAHA I DID IT!
    write_recipe_info(recipe_dict)


def main():
    ua = UserAgent()
    headers = {'user-agent': ua.random}
    page_link = 'http://allrecipes.com/'
    page = requests.get(page_link, headers=headers, timeout=5)
    print(page)

    '''
    
    # grab_links(1)
    start = time.time()
    # grab_all_recipes()
    grab_links(10)
    end = time.time()
    print("Elapsed time (sec): ")
    print(end - start)
    '''


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    main()
