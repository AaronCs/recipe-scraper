from lxml import html
from queue import Queue
import threading
import requests
import logging
import json

# Scrapes recipes off of allrecipes.com
# Go to a maximum of 100 pages.


def get_links(page_num, recipe_array):
    # Grabs all links on a page, and then appends it to a list.
    # The list will later be written into a file.
    page_link = 'http://allrecipes.com/recipes/?page={0}#{0}'.format(page_num)
    page = requests.get(page_link, timeout=5)
    tree = html.fromstring(page.content)
    links = tree.xpath("//article[@class='grid-col--fixed-tiles']/a/@href")
    for i in links:
        recipe_array.append(i)
    # logging.info(links)

    """
    categories = tree.xpath("//a[@class='hero-link__item']/span/text()")
    links = tree.xpath("//a[@class='hero-link__item']/@href")
    """

    # return links


def write_recipe_links(recipe_array):
    # Write to a file.
    opened_file = open("recipe_links.txt", "w", encoding="utf-8")
    # TODO: Change mode to append.
    with opened_file as file:
        for link in recipe_array:
            file.write(link)
            file.write('\n')  # Newline as the delimiter.


def write_recipe_info(recipe):
    # Saves recipe info into a json file.
    # Recipe is a dictionary (object, json)
    opened_file = open("recipes.json", "a", encoding="utf-8")
    with opened_file as file:
        json.dump(recipe, file)


def parse_recipe(link, recipe_dict):
    # Parses the recipe ingredients and steps.
    to_parse = 'http://allrecipes.com{0}'.format(link).rstrip()  # rstrip removes the newline.
    page = requests.get(to_parse, timeout=5)
    tree = html.fromstring(page.content)
    title = tree.xpath("//h1[@class='recipe-summary__h1']/text()")
    ingredients = tree.xpath("//span[@itemprop='ingredients']/text()")
    directions = tree.xpath("//span[@class='recipe-directions__list--item']/text()")
    # Store results in a dictionary.
    recipe_dict[title[0]] = {'ingredients': ingredients, 'directions': directions}

# def populate_queue(page):
    # Populates the queue with recipe links, starting from the page in the arg.


def load_recipe_links(recipe_queue):
    # Loads recipes into the queue.
    opened_file = open("recipe_links.txt", "r", encoding="utf-8")
    with opened_file as file:
        for link in file:
            recipe_queue.put(link)


def grab_links(num_links):
    # Put links into an array, and then write the entire array.
    link_array = []
    for i in range(num_links):
        get_links(i, link_array)   # Make this portion multithreaded.
    link_array = list(set(link_array))  # Remove duplicates. Seems like a hack.
    write_recipe_links(link_array)


def grab_all_recipes():
    # It's like main, but for recipes, not recipe links.
    recipe_queue = Queue()
    load_recipe_links(recipe_queue)
    recipe_dict = {}
    #while not recipe_queue.empty():
    parse_recipe(recipe_queue.get(), recipe_dict)


def main():
    grab_all_recipes()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    main()
