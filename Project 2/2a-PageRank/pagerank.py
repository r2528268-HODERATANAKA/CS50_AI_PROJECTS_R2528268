import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    all_pages = list(corpus)
    links = get_links(corpus, page)

    # Every page gets a small share for the random jump
    probabilities = {}
    for p in all_pages:
        probabilities[p] = (1 - damping_factor) / len(all_pages)

    # Pages linked from the current page share the rest equally
    for link in links:
        probabilities[link] += damping_factor / len(links)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    counts = {page: 0 for page in corpus}

    # Start on a random page
    page = random.choice(list(corpus))

    for _ in range(n):
        counts[page] += 1

        # Pick the next page using the transition model
        probabilities = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probabilities),
                              weights=list(probabilities.values()))[0]


    return {page: counts[page] / n for page in corpus}

def iterate_pagerank(corpus, damping_factor):
    num_pages = len(corpus)

    # Start with every page equal
    ranks = {page: 1 / num_pages for page in corpus}

    while True:
        new_ranks = {}

        for page in corpus:
            # Part 1: random jump to any page
            rank = (1 - damping_factor) / num_pages

            # Part 2: add a share from every page that links here
            for other in corpus:
                other_links = get_links(corpus, other)
                if page in other_links:
                    rank += damping_factor * ranks[other] / len(other_links)

            new_ranks[page] = rank

        # Stop when no rank changed by more than 0.001
        done = all(abs(new_ranks[p] - ranks[p]) <= 0.001 for p in corpus)
        ranks = new_ranks
        if done:
            return ranks


def get_links(corpus, page):

    # Function to return the pages that page links to.

    if len(corpus[page]) == 0:
        return set(corpus)
    return corpus[page]


if __name__ == "__main__":
    main()
