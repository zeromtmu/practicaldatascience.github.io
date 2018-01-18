#!/usr/bin/env python
import sys
from Queue import PriorityQueue

def boolean_retrieval(inverted_list, q_words):
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
        cur_doc = inverted_list[words[i]][0]
        PQ.put((cur_doc, i))
        cur_max_doc = max(cur_max_doc, cur_doc)
    while True:
        cur_min_doc, id = PQ.get()
        if cur_min_doc == cur_max_doc:
            ret.append(cur_min_doc)
        idx[id] += 1
        if idx[id] >= len(inverted_list[words[id]]):
            return ret
        next_doc = inverted_list[words[id]][idx[id]]
        cur_max_doc = max(cur_max_doc, next_doc)
        PQ.put((next_doc, id))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "inverted file name needed."
        exit()
    
    # read inverted list from file specific by first arg
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
        doc = boolean_retrieval(inverted_list, q_words)
        print doc
        q_line = sys.stdin.readline()
