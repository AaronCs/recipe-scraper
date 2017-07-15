from queue import Queue
import threading
import time
import logging

# Learning threading
print_lock = threading.Lock()  # Prevents threads from running over each other
q = Queue()

'''

def example_job(worker):
    time.sleep(0.5)  # pretend to do work.
    with print_lock:
        print(threading.current_thread(), worker)


# The threader pulls a worker from the queue and then processes it.
def threader():
    while True:
        # Get a worker from the queue
        worker = q.get()
        example_job(worker) # Does work inside here
        q.task_done()

'''


def thread_manager(num):
    # Sort of like middleware for threaders.
    while True:
        worker = q.get()
        my_function(num)
        q.task_done()


def my_function(num):
    with print_lock:
        # If this lock wasn't here, then one thread might lock out all the others.
        time.sleep(0.5)
        print("Hello World! My number is: ", num)


def main():
    logging.basicConfig(level=logging.DEBUG)
    for x in range(20):
        t = threading.Thread(target=thread_manager, args=(x,))  # This is a Thread object.
        # args argument requires a tuple, so (x,) is a tuple, while (x) is the value x.
        # Target is the callable object invoked by the run() method
        # run() method represents the thread's activity.

        # Classify as daemon so that they will die once main dies.
        t.daemon = True
        t.start()

    start = time.time()
    # What exactly does this do?
    for worker in range(20):
        q.put(worker)
    q.join()
    # The join() method blocks the rest of main from happening until the thread is done.
    # Basically, the main thread waits until q is done.
    # This thing blocks until all items in the queue have been get() and processed.
    print("Done!")
    print('Time: ', time.time() - start)


if __name__ == '__main__':
    main()
