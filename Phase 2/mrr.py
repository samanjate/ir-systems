from bs4 import BeautifulSoup
import urllib2
import time
import os
import re
import sys
import glob
import operator
import csv
import collections

## in the below code we are creating a relevantset
## each of the key will be the query_id
## and the values will be the relevant documents for it
## e.g 1 = {doc1 , doc2 , doc3}
## 1 is the query id and doc1 etc are the relevant documents
## the same is done for the irrelevant documents

precisiondict = {}
recalldict = {}
Reciprocalrank = {}
Averageprecision = {}

def create_set_rel(f,setboolean):
    mapping_dict = {}
    for line in f:
        templist = line.split()
        key = templist[0]
        value = templist[2]
        if setboolean:
            value = value[5:]
        if key not in mapping_dict:
            mapping_dict[key] = []
            mapping_dict[key].append(value)
        else:
            mapping_dict[key].append(value)
    return mapping_dict


def calculateprecision(relevantset , irrelevantset):
    ## precisiondict will have key as query id and its list of
    ## precision at each relevant document achieved
    ## same is applicable for the recalldict

    for key in irrelevantset:
        total_till = 0.0
        rel_till = 0.0
        Precision_sum = 0
        curr_doc_type = False
        if key in relevantset:
                relevantvalues = relevantset[key]
        else:
            continue
        precisiondict[key] = []
        recalldict[key] = []
        First_Relevant_found = False
        irrelevantvalues = irrelevantset[key]
        total_rel_doc = len(relevantvalues)
        for curr_doc in irrelevantvalues:
            total_till = total_till + 1
            if curr_doc in relevantvalues:
                curr_doc_type = True
                if not First_Relevant_found:
                    recirank = 1 / total_till
                    Reciprocalrank[key] = recirank
                    First_Relevant_found = True
                rel_till = rel_till + 1
            precision = rel_till / total_till
            if curr_doc_type:
                Precision_sum = Precision_sum + precision
            recall = rel_till / total_rel_doc
            precisiondict[key].append(precision)
            recalldict[key].append(recall)
            curr_doc_type = False
        Averageprecision[key] = Precision_sum / total_rel_doc

if __name__ == "__main__":
    SetBoolean = True
    f = open('cacm.txt', 'r')
    relevantset = create_set_rel(f , SetBoolean)
    SetBoolean = False
    f = open('retres.txt', 'r')
    irrelevantset = create_set_rel(f, SetBoolean)
    calculateprecision(relevantset ,irrelevantset)
    Sortedprecdict = collections.OrderedDict(sorted(precisiondict.items()))
    Sortedrecalldict = collections.OrderedDict(sorted(recalldict.items()))
    '''
    print precisiondict
    print recalldict
    print Reciprocalrank
    print Averageprecision
    '''
    with open('precisiondict.csv', 'w') as f:
        c = csv.writer(f)
        for key, value in Sortedprecdict.items():
            c.writerow([key] + value)
