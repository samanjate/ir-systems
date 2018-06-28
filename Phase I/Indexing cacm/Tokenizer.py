from bs4 import BeautifulSoup
import re
import os

def cleanText(text):
    text = text.lower()
    text = re.sub('\[(.*?)\]', '', text)
    text = re.sub('[\"\(\)]', '', text)
    text = re.sub('(\'[a-zA-Z]+)', '', text)
    text = re.sub('[^\x00-\x7F]+', '', text)
    text = re.sub('[^a-zA-Z0-9]+$', '', text)
    if (not any(char.isdigit() for char in text)):
        text = re.sub('[^a-zA-Z0-9-]', '', text)
    text = re.sub('.*www.*|.*http.*', '', text)
    text = re.sub('^[~{}&\'*+-/].*', '', text)
    return text

if __name__ == '__main__':
    path = 'cacm/'
    duplicatefile = []
    for filesname in os.listdir(path):
        f = open(path+filesname, 'r')
        htmltext = f.read()
        soup = BeautifulSoup(htmltext, "html.parser")
        filename = filesname.split('.')[0]+'.txt'
        filetext = []
        for tag in soup.findAll('pre'):
            filetext = tag.text.split()
        for token in xrange(len(filetext)):
            filetext[token] = cleanText(filetext[token])
        fileref = open(filename, 'w')
        for token in filetext:
            if token != "":
                fileref.write(token+"\n")
        fileref.close()
