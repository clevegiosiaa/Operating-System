from queue import Queue
import random

# Function to find page faults using FIFO
def FIFOpageFaults(pages, n, capacity):
    s = set()

    indexes = Queue()

    # Start from initial page
    page_faults = 0
    for i in range(n):
        # Check if the set can hold more pages
        if len(s) < capacity:
            # Insert it into set if not present already which represents page fault
            if pages[i] not in s:
                s.add(pages[i])
                # increment page fault
                page_faults += 1

                # Push the current page into the queue
                indexes.put(pages[i])
        # If the set is full then need to perform FIFO
        else:
            # Check if current page is not already present in the set
            if pages[i] not in s:
                # Pop the first page from the queue
                val = indexes.queue[0]
                indexes.get()
                # Remove the indexes page
                s.remove(val)
                # insert the current page
                s.add(pages[i])
                # push the current page into the queue
                indexes.put(pages[i])
                # Increment page faults
                page_faults += 1

    return page_faults


def LRUpageFaults(pages, capacity):
    # List of current pages in Main Memory
    s = []
    pageFaults = 0
    # pageHits = 0
    for i in pages:
        # If i is not present in currentPages list
        if i not in s:
            # Check if the list can hold equal pages
            if len(s) == capacity:
                s.remove(s[0])
                s.append(i)
            else:
                s.append(i)
            # Increment Page faults
            pageFaults += 1
        # If page is already there in currentPages
        else:
            # Remove previous index of current page
            s.remove(i)
            # Now append it, at last index
            s.append(i)

    return pageFaults


# main program
if __name__ == "__main__":
    pages = []
    for i in range(random.randint(10, 20)):
        pages.append(random.randint(0, 9))
    print("Pages: ", pages)
    
    n = len(pages)
    capacity = 4

    print("Page Faults w/ FIFO: ", FIFOpageFaults(pages, n, capacity))
    print("Page Faults w/ LRU: ", LRUpageFaults(pages, capacity))
