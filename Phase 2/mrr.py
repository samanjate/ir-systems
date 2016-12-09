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

def create_set_rel(f):
    mapping_dict = {}
    for line in f:
        templist = line.split()
        key = templist[0]
        key = int(key)
        value = templist[2]
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
                ## below if clause is used to calculate
                ## the Reciprocalrank
                if not First_Relevant_found:
                    recirank = 1 / total_till
                    Reciprocalrank[key] = recirank
                    First_Relevant_found = True
                ## reciprocal is calculated in the above rank
                rel_till = rel_till + 1
            precision = rel_till / total_till
            if curr_doc_type:
                Precision_sum = Precision_sum + precision
            recall = rel_till / total_rel_doc
            precisiondict[key].append(precision)
            recalldict[key].append(recall)
            curr_doc_type = False
        Averageprecision[key] = Precision_sum / total_rel_doc

def load_relavtive_docs():
    relavent_documents = {}
    with open('cacm.txt') as doc_list:
        for entry in doc_list:
            words = entry.split()
            q_id = int(words[0])
            if q_id not in relavent_documents:
                relavent_documents[q_id] = ['CACM-'+'{0:04}'.format(int(words[2].lstrip('CACM-')))]
            else:
                relavent_documents[q_id].append('CACM-'+'{0:04}'.format(int(words[2].lstrip('CACM-'))))

    return relavent_documents


if __name__ == "__main__":
    relevantset = load_relavtive_docs()
    f = open('cacm_queries_bm25_stop.txt', 'r')
    irrelevantset = create_set_rel(f)
    calculateprecision(relevantset ,irrelevantset)
    Sortedprecdict = collections.OrderedDict(sorted(precisiondict.items()))
    Sortedrecalldict = collections.OrderedDict(sorted(recalldict.items()))
    
    '''
    with open('precision_dict_cacm_queries_bm25_stop.csv', 'w') as f:
        c = csv.writer(f)
        for key, value in Sortedprecdict.items():
            c.writerow([key] + value)

    with open('recall_dict_cacm_queries_bm25_stop.csv', 'w') as f:
        c = csv.writer(f)
        for key, value in Sortedrecalldict.items():
            c.writerow([key] + value)

    with open('MRR_BM25_stop.txt', 'w') as f:
        sum_reciprocal = 0.0
        sum_precision = 0.0
        total_rec_values = len(Reciprocalrank)
        total_avg_values = len(Averageprecision)
        for key in Reciprocalrank:
            sum_reciprocal = sum_reciprocal + Reciprocalrank[key]
        for key in Averageprecision:
            sum_precision = sum_precision + Averageprecision[key]
        meanavp = sum_precision/total_avg_values
        meanrec = sum_reciprocal/total_rec_values
        f.write("Mean average precision for BM25 with stopping is "+ "->" + '\t')
        f.write(str(meanavp))
        f.write("\n")
        f.write("Mean reciprocal rank for BM25 with stopping  is "+ "->" + '\t')
        f.write(str(meanrec))
        f.write("\n")
        sort_pr = sorted(precisiondict.items(), key=operator.itemgetter(0))
        for key in sort_pr:
            print key[0]
            values = key[1]
            prec5 = values[4]
            prec19 = values[19]
            f.write("For Query id:"+ " " + str(key[0]) + " ")
            f.write("precision at 5th rank is: "+ "->" + '\t')
            f.write(str(prec5)+ "\n")
            f.write("For Query id:"+ " " + str(key[0]) + " ")
            f.write("precision at 20th rank is: "+ "->" + '\t')
            f.write(str(prec19)+"\n")
    '''
