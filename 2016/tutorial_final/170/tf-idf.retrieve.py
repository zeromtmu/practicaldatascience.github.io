#!/usr/bin/env python
import sys
from Queue import PriorityQueue
import math

def tf_idf_retrieval(inverted_list, q_words):
    # get the total size of the documents
    N = len(reduce(lambda x, y: x | y,
               map(lambda i: set(map(lambda j: j.split(',')[0], i)),
                   inverted_list.values())))
    words, ret = [], []
    for word in q_words:
        if word not in inverted_list:
            return ret
        words.append(word)
    n = len(words)

    # current index for each id
    idx = [0] * n

    # initialize priority queue
    # in PQ, (current_word, id) is stored
    # cur_max_word stores the maximum word in PQ
    PQ = PriorityQueue()
    cur_max_doc = ""
    for i in range(n):
        cur_doc = inverted_list[words[i]][0].split(',')[0]
        PQ.put((cur_doc, i))
        cur_max_doc = max(cur_max_doc, cur_doc)
    while True:
        cur_min_doc, id = PQ.get()
        if cur_min_doc == cur_max_doc:
            # calculate the sum of tf-idf score of all q_word
            sum_tfidf = 0.0
            for i in range(n):
                tf = float(inverted_list[words[i]][idx[i]].split(',')[1])
                df = len(inverted_list[words[i]])
                idf = math.log(1.0 * N / df)
                sum_tfidf += tf * idf
            ret.append((sum_tfidf, cur_min_doc))
        idx[id] += 1
        if idx[id] >= len(inverted_list[words[id]]):
            # sort the result, and then output
            ret.sort(reverse=True)
            return ret
        next_doc = inverted_list[words[id]][idx[id]].split(',')[0]
        cur_max_doc = max(cur_max_doc, next_doc)
        PQ.put((next_doc, id))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "inverted file name needed."
        exit()
    inverted_list = {}
    file = open(sys.argv[1], "r")
    line = file.readline()
    while line:
        parts = line.strip().split(" ")
        inverted_list[parts[0]] = parts[1:]
        line = file.readline()

    q_line = sys.stdin.readline()
    while q_line:
        q_words = q_line.strip().split(" ")
        doc = tf_idf_retrieval(inverted_list, q_words)
        print doc
        q_line = sys.stdin.readline()
