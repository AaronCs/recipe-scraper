from lxml import html
from queue import Queue
import threading
import requests
import logging

# I probably don't need to figure out the maximum recipe pages there are, but
# it seems like a good way to test out threading.

worker_queue = Queue()
worker_lock = threading.Lock()


def find_max_pages(i):
    # Change page_link to find max pages of different things.
    page_link = 'http://allrecipes.com/recipes/?page={0}#{0}'.format(i)
    page = requests.get(page_link, timeout=5)

    if page.status_code != 200:
        # Checks the status code to see if it's a good idea to continue.
        return False

    tree = html.fromstring(page.content)
    error_page = tree.xpath('//section[@class="error-page"]')
    # TODO: Modify things to make it multi-threaded.
    if error_page:
        return i
    if i > 1000:
        return find_max_pages(i + 500)
    return find_max_pages(i + 100)


def max_page_worker(page_num):
    with worker_lock:
        find_max_pages(page_num)


def threader(num_threads):
    # Put numbers in the queue and have the workers go through it?
    for i in range(500):
        worker_queue.put(i)
    for i in range(num_threads + 1):
        # TODO: Modify args into something else.
        # i.e: if another worker is already on that number, then skip ahead.
        # TODO: Figure out how to return numbers.
        thread = threading.Thread(target=max_page_worker, args=(i,))
        thread.daemon = True
        thread.start()


def main():
    threader(10)

if __name__ == "__main__":
    main()
