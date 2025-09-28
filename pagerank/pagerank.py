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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Copus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    # The page is a string representing which page the random surfer is currently on.
    # The dampin factor is a floating point number representing the damping factor to be used when generating the probabilities.

    # The return value should be a python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing the
    # probability that a random surfer would choose that page next. The values in this return probability distribution should sum to 1.
    prob_dist = dict()
    n_pages = len(corpus)  # total number of pages in the corpus
    linked_pages = corpus[page]  # set of all pages linked to by the current page

    if len(linked_pages) == 0:
        # if the current page has no outgoing link, we need to treat it as having links to all pages in the corpus
        for p in corpus:
            prob_dist[p] = (
                1 / n_pages
            )  # randomly choose any page from the corpus with equal probability
        return prob_dist

    # Now we will treat the case where the current page has outgoing links
    base_prob = (
        1 - damping_factor
    ) / n_pages  # base probability for each page from the corpus
    linked_prob = damping_factor / len(
        linked_pages
    )  # additional probability for each linked page
    for p in corpus:
        prob_dist[p] = base_prob
        if p in linked_pages:
            prob_dist[p] += linked_prob
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    # The damping factor is a floating point number representing the damping factor to be used by the transition model.
    # The n is an integer representing the number of samples that should be generated to estimate PageRank values.

    # The return value should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representign,
    # that page's estimated PageRank value (a value between 0 and 1). All PageRank values should sum to 1.
    page_rank = dict()

    # Initialize the first sample by randomly choosing a page from the corpus
    current_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        if current_page in page_rank:
            page_rank[current_page] += 1
        else:
            page_rank[current_page] = 1

        # Use the transition model to get the probability distribution for the next page
        prob_dist = transition_model(corpus, current_page, damping_factor)
        # Chose randomly the next page based on the probability distribution
        pages = list(prob_dist.keys())
        probabilities = list(prob_dist.values())
        current_page = random.choices(pages, weights=probabilities, k=1)[0]

    # Normalization of the page rank values that we have so far.
    for page in page_rank:
        page_rank[page] = page_rank[page] / n

    # If some page was never visited during the sampling, it won't be in the page_rank dictionary yet.
    # We need to add it with a PageRank value of 0.
    for page in corpus:
        if page not in page_rank:
            page_rank[page] = 0

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    # The damping factor is a floating point number representing the damping factor to be used by the transition model.

    # The return value should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing,
    # that page's estimated PageRank value (a value between 0 and 1). All PageRank values should sum to 1.

    page_rank = dict()
    n_pages = len(corpus)

    # Initialize the page rank values to 1/N for each page in the corpus
    for page in corpus:
        page_rank[page] = 1 / n_pages

    # Iteratively update the page rank values until convergence
    converged = False
    while not converged:
        new_page_rank = dict()
        converged = True
        for page in corpus:
            # Calculate the new PageRank value for the page using the Background formula.
            # The formula is PR(p) = (1-d)/N + d * sum(PR(i)/NumLinks(i)) for all pages i that link to p.

            # start with the base probability
            new_page_rank[page] = (1 - damping_factor) / n_pages
            # Now we need to add the sum of the contributions from all pages that link to the current page
            for i in corpus:
                if page in corpus[i]:
                    new_page_rank[page] += damping_factor * (
                        page_rank[i] / len(corpus[i])
                    )
                # If a page has no outgoing links, we treat it as having links to all pages
                if len(corpus[i]) == 0:
                    new_page_rank[page] += damping_factor * (page_rank[i] / n_pages)
            # Check if the PageRank value has converged (changed by less than 0.001)
            if abs(new_page_rank[page] - page_rank[page]) >= 0.001:
                converged = False
        page_rank = new_page_rank
    return page_rank


if __name__ == "__main__":
    main()
