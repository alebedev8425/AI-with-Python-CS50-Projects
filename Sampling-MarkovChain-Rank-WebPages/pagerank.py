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
    prob = transition_model(corpus, "1.html", .85)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(prob)
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
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    prob = dict()

    if page not in corpus:
        raise KeyError(f"Page {page} is not in corpus")
    links = corpus[page]
    if len(links) == 0:
        for filename in corpus:
            prob[filename] = 1.0 / len(corpus)
        return prob
    else:
        for filename in corpus:
            prob[filename] = (1 - damping_factor) / len(corpus)
        for filename in links:
            prob[filename] += damping_factor / len(links)
        return prob



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ranks = {p: 0 for p in corpus}
    page = random.choice(list(corpus))
    ranks[page] += 1 # count first page
    for _ in range(n - 1):
        dist = transition_model(corpus, page, damping_factor)

        pages = list(dist.keys())
        weights = list(dist.values())
        page = random.choices(pages, weights=weights, k=1)[0]
        ranks[page] += 1

    # get the real value after dividing by size of sample
    for page in ranks:
        ranks[page] /= n

    return ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    ranks = {p: 1/len(corpus) for p in corpus}
    while True:
        new_ranks = dict()
        for p in corpus:
            total = 0.0

            for q in corpus:
                if len(corpus[q]) == 0: # no links
                    total += ranks[q] / N
                elif p in corpus[q]:
                    total += ranks[q] / len(corpus[q])

            new_ranks[p] = (1 - damping_factor) / N + damping_factor * total

        # check if we done
        if all(abs(new_ranks[p] - ranks[p]) < .0001 for p in new_ranks):
            return new_ranks

        ranks = new_ranks

if __name__ == "__main__":
    main()
