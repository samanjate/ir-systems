from bs4 import BeautifulSoup
import urllib2
import time
import os
import re
import sys
import glob
import operator

## in the below code we are creating a relevantset
## each of the key will be the query_id
## and the values will be the relevant documents for it
## e.g 1 = {doc1 , doc2 , doc3}
## 1 is the query id and doc1 etc are the relevant documents
## the same is done for the irrelevant documents

def create_set_rel_irre(f):
    mapping_dict = {}
    for line in f:
        templist = line.split()
        key = templist[0]
        value = templist[2]
        if key not in mapping_dict:
            mapping_dict[key] = []
            mapping_dict[key].append(value)
        else:
            mapping_dict[key].append(value)
    return mapping_dict

def calculateprecision(relevantset , irrelevantset):
    precisiondict = {}
    for key in irrelevantset:
        total_till = 0.0
        rel_till = 0.0
        precisiondict[key] = []
        irrelevantvalues = irrelevantset[key]
        relevantvalues = relevantset[key]
        for curr_doc in irrelevantvalues:
            total_till = total_till + 1
            if curr_doc in relevantvalues:
                rel_till = rel_till + 1
                precision = rel_till / total_till
                precisiondict[key].append(precision)
    return precisiondict


if __name__ == "__main__":
    f = open('cacm.txt', 'r')
    relevantset = create_set_rel_irre(f)
    f = open('retres.txt', 'r')
    irrelevantset = create_set_rel_irre(f)
    precisiondict = calculateprecision(relevantset , irrelevantset)
