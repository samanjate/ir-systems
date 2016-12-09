from bs4 import BeautifulSoup
import urllib2
import time
import os
import re
import sys
import glob
import operator
import logging
import copy
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.summarization import summarize
from nltk.tokenize import TweetTokenizer
from collections import Counter

common_words = []

def parseddoc(doc_id):
    doc_id = "CACM" + "-" + doc_id + ".html"
    return doc_id

## below fucnction will get the title for
## the given document

def get_Title(a):
    Title = ""
    StringOfLines  = a.split('\n')
    index = 0
    for value in StringOfLines:
      if value is  '':
        index = index + 1
      else:
        break
    for value in range(index ,len(StringOfLines)):
      if StringOfLines[value] is not '':
        Title = Title + StringOfLines[value]
      else:
        break
    return Title

def load_common_words():
    with open("common_words.txt") as words:
        for word in words:
            common_words.append(word.split()[0])

## below fucnction will get the sentences for the given documents
## and return them as the sentences
def get_Sentences(a):
  StringOfLines = a.split('\n')
  index = 0
  String = ""
  for value in StringOfLines:
      if value is  '':
        index = index + 1
      else:
        break
  secondaryindex = index
  for value in range(index ,len(StringOfLines)):
      if StringOfLines[value] is not '':
          secondaryindex = secondaryindex + 1
      else:
        break
  for value in range(secondaryindex+1 , len(StringOfLines)):
      String = String + " " + StringOfLines[value]
  String = String.replace("\t", " ")
  sentences = re.split(r' *[\.\?!][\'"\)\]]* *', String)
  return sentences

def calculate_sen_score(Word_count_map , Sentences):
    ## key is the sentence index in the list of sentences
    ## value is the score for that sentence
    Sentence_Score = {}
    for index in range(0 ,len(Sentences)):
        sent_score = 0
        sentence = Sentences[index]
        ## splitting the sentence into its token
        sentence_token = sentence.split(' ')
        for token in sentence_token:
            if token in Word_count_map:
                sent_score = sent_score + 1
        ## all the data is being stored in the sentence score and
        ## we will return this hashmap to the user.
        Sentence_Score[index] = sent_score
    return Sentence_Score




if __name__ == "__main__":
    load_common_words()
    Word_count_map = {}
    Token_count_map = {}
    Finalstring = ""
    doc_id = "1134"
    tknzr = TweetTokenizer()
    Sentences = []
    FinalSnippet = ""
    query = " Intermediate languages used in construction of multi-targeted compilers; TCOLL"
    ## splitting the query into the query terms and making all of them lowercase
    queryset = tknzr.tokenize(query)
    if ',' in queryset:
        queryset.remove(',')
    if ';' in queryset:
        queryset.remove(';')
    if ':' in queryset:
        queryset.remove(':')
    tempqueryset = [element.lower() for element in queryset]
    queryset = []
    for query_term in tempqueryset:
        if query_term not in common_words:
            queryset.append(query_term)
    queryset = set(queryset)
    ## got the query terms and split them into the respective tokens
    modified_doc_id = parseddoc(doc_id)
    a = open(modified_doc_id,'rb')
    soup = BeautifulSoup(a.read(),"html.parser")
    for i in soup.findAll('pre'):
        a = i.getText().encode('utf-8')
        b = a
        ## retrieving the tokes from the document set
        tokens = tknzr.tokenize(b)
        tokens = [element.lower() for element in tokens]
        tokenset = set(tokens)
        ## retrieved the tokens and converted them to token list
        ## get the title for the given document i.e the first sentence
        Title = get_Title(a)
        FinalSnippet = FinalSnippet + Title

        ## got all the subsequent sentences i.e the one after the first sentence
        Sentences = get_Sentences(a)
        print Sentences
        ## getting the query terms whihc are present in the set of tokes
        ## for the given  query and given document
        u = set.intersection(queryset, tokenset)
        print u
        for token in tokens:
          if token in Token_count_map:
              val = Token_count_map[token]
              val = val + 1
              Token_count_map[token] = val
          else:
              Token_count_map[token] = 1
        for word in  u:
          freq = Token_count_map[word]
         ## assuming frequecy words between 1 and 3 are relevant for
         ## snippet generation.

          if (freq > 1 and freq <= 3):
              Word_count_map[word] = freq
              
    if len(Sentences) > 2:
        Sentences_Score = calculate_sen_score(Word_count_map , Sentences)
        sorted_sentences = sorted(Sentences_Score.items(), key=operator.itemgetter(1) ,reverse=True)
        for x in range(0,2):
            FinalSnippet = FinalSnippet + Sentences[sorted_sentences[x][0]] + "."
    else:
        for x in range(0 ,len(Sentences)-1):
            FinalSnippet = FinalSnippet + Sentences[x]+ "."
    TempFinalSnippet = FinalSnippet.split(' ')
    FinalSnippet = ""
    for word in TempFinalSnippet:
        if word in Word_count_map:
            word = word.upper()
            FinalSnippet = FinalSnippet + word + " "
        else:
            FinalSnippet = FinalSnippet + word + " "
    print FinalSnippet
