from bs4 import BeautifulSoup
import urllib2
import time
import os
import re
import sys
import glob
import operator
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.summarization import summarize
from nltk.tokenize import TweetTokenizer
from collections import Counter


def parseddoc(doc_id):
    doc_id = "CACM" + "-" + doc_id + ".html"
    return doc_id

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
      String = String+StringOfLines[value]
  String = String.replace("\t", " ")
  sentences = re.split(r' *[\.\?!][\'"\)\]]* *', String)
  return sentences

if __name__ == "__main__":
   Finalstring = ""
   doc_id = "2004"
   Sentences = []
   modified_doc_id = parseddoc(doc_id)
   a = open(modified_doc_id,'rb')
   soup = BeautifulSoup(a.read(),"html.parser")
   for i in soup.findAll('pre'):
        a = i.getText().encode('utf-8')
        b = a
        tknzr = TweetTokenizer()
        tokens = tknzr.tokenize(b)
        Title = get_Title(a)
        Sentences = get_Sentences(a)
        sd = len(Sentences) + 1
        countoken = Counter(tokens)
        print countoken
        print sd



   #print StringOfLines
   '''
   for sentence in Sentences:
       print "new sentence started"
       print sentence
   '''
