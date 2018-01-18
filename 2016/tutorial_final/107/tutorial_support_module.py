import re
import collections # optional, but we found the collections.Counter object useful
import scipy.sparse as sp
import numpy as np
import math
import random


#code given in assignment 3 - used to load the federalist papers corpus for demonstration purposes. 
def load_federalist_corpus(filename):
    """ Load the federalist papers as a tokenized list of strings, one for each essay"""
    with open(filename, "rt") as f:
        data = f.read()
    papers = data.split("FEDERALIST")
    
    # all start with "To the people of the State of New York:" (sometimes . instead of :)
    # all end with PUBLIUS (or no end at all)
    locations = [(i,[-1] + [m.end()+1 for m in re.finditer(r"of the State of New York", p)],
                 [-1] + [m.start() for m in re.finditer(r"PUBLIUS", p)]) for i,p in enumerate(papers)]
    papers_content = [papers[i][max(loc[1]):max(loc[2])] for i,loc in enumerate(locations)]

    # discard entries that are not actually a paper
    papers_content = [p for p in papers_content if len(p) > 0]

    # replace all whitespace with a single space
    papers_content = [re.sub(r"\s+", " ", p).lower() for p in papers_content]

    # add spaces before all punctuation, so they are separate tokens
    punctuation = set(re.findall(r"[^\w\s]+", " ".join(papers_content))) - {"-","'"}
    for c in punctuation:
        papers_content = [p.replace(c, " "+c+" ") for p in papers_content]
    papers_content = [re.sub(r"\s+", " ", p).lower().strip() for p in papers_content]
    
    authors = [tuple(re.findall("MADISON|JAY|HAMILTON", a)) for a in papers]
    authors = [a for a in authors if len(a) > 0]
    
    numbers = [re.search(r"No\. \d+", p).group(0) for p in papers if re.search(r"No\. \d+", p)]
    
    return papers_content, authors, numbers


###############################################################################
###############################################################################
################ Support code written for K-Means implementation ##############
###############################################################################
###############################################################################
