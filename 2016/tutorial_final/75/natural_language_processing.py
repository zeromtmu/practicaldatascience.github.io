
# coding: utf-8

# # Natural Language Processing (688 only) [35pts]
# ## Introduction
# 
# In this problem you will develop two techniques for analyzing free text documents: a bag of words approach based upon creating a TFIDF matrix, and an n-gram language model.
# 
# You'll be applying your models to the text from the Federalist Papers.  The Federalist papers were a series of essay written in 1787 and 1788 by Alexander Hamilton, James Madison, and John Jay (they were published anonymously at the time), that promoted the ratification of the U.S. Constitution.  If you're curious, you can read more about them here: https://en.wikipedia.org/wiki/The_Federalist_Papers . They are a particularly interesting data set, because although the authorship of most of the essays has been long known since around the deaths of Hamilton and Madison, there was still some question about the authorship of certain articles into the 20th century.  You'll use document vectors and language models to do this analysis for yourself.

# ## The dataset
# 
# You'll use a copy of the Federalist Papers downloaded from Project Guttenberg, available here: http://www.gutenberg.org/ebooks/18 .  Specifically, the "pg18.txt" file included with the homework is the raw text downloaded from Project Guttenberg.  To ensure that everyone starts with the exact same corpus, we are providing you the code to load and tokenize this document, as given below.

# In[ ]:

import re

def load_federalist_corpus(filename):
    """ Load the federalist papers as a tokenized list of strings, one for each eassay"""
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
    
    


# In[ ]:

# AUTOLAB_IGNORE_START
# AUTOLAB_IGNORE_STOP


# You're welcome to dig through the code here if you're curious, but it's more important that you look at the objects that the function returns.  The `papers` object is a list of strings, each one containing the full content of one of the Federalist Papers.  All tokens (words) in the text are separated by a single space (this includes some puncutation tokens, which have been modified to include spaces both before and after the punctuation. The `authors` object is a list of lists, which each list contains the author (or potential authors) of a given paper.  Finally the `numbers` list just contains the number of each Federalist paper.  You won't need to use this last one, but you may be curious to compare the results of your textual analysis to the opinion of historians.

# ## Q1: Bag of words, and TFIDF [6+6pts]
# 
# In this portion of the question, you'll use a bag of words model to describe the corpus, and write routines to build a TFIDF matrix and a cosine similarity function.  Specifically, you should first implement the TFIDF function below.  This should return a _sparse_ TFIDF matrix (as for the Graph Library assignment, make sure to directly create a sparse matrix using `scipy.sparse.coo_matrix()` rather than create a dense matrix and then convert it to be sparse).
# 
# Important: make sure you do _not_ include the empty token `""` as one of your terms. 

# In[ ]:

import collections # optional, but we found the collections.Counter object useful
import scipy.sparse as sp
import numpy as np

def tfidf(docs):
    """
    Create TFIDF matrix.  This function creates a TFIDF matrix from the
    docs input.

    Args:
        docs: list of strings, where each string represents a space-separated
              document
    
    Returns: tuple: (tfidf, all_words)
        tfidf: sparse matrix (in any scipy sparse format) of size (# docs) x
               (# total unique words), where i,j entry is TFIDF score for 
               document i and term j
        all_words: list of strings, where the ith element indicates the word
                   that corresponds to the ith column in the TFIDF matrix
    """
    all_words = []
    words_idx = {}
    words_doc = {}
    
    cnts = []
    
    for d in docs:
        cnt = collections.Counter(d.split())
        cnts.append(cnt)
        for w in cnt:
            if w not in words_idx:
                all_words.append(w)
                words_idx[w] = len(all_words)-1
            
            
    shape = (len(docs), len(all_words))
    tf = sp.coo_matrix(shape)
    tf= tf.tolil()
    for i in range(shape[0]):
        cnt = cnts[i]
        for w in cnt:
            tf[i, words_idx[w]] = cnt[w]
            
            if w in words_doc:
                words_doc[w].append(i)
            else:
                words_doc[w] = [i]
    
    
    idf = sp.coo_matrix((shape[1], 1))
    idf = idf.tolil()
    for i in range(shape[1]):
        idf[i, 0] = np.log(shape[0] / float(len(words_doc[all_words[i]])))
    
    idfT = idf.transpose()

    
    tfidf = tf.multiply(idfT)
    
    return tfidf.tocoo(), all_words
        


