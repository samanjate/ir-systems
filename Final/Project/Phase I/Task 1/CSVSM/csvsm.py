import re
import math
import operator

inverted_index = {}
N = 3204.0 #number of documents in the corpus
document_weigths = {}
all_document_weigths = {}
query_weights = {}
query_term_frequency = {}
cosine_scores = {}
denominator_for_docs = {}

def load_inverted_index(inverted_index):
    with open('inverted_index.txt') as index:
        for entry in index:
            word = entry.split("->")[0].strip(' ')
            entry = re.sub("[(,)>-]", "", entry)
            data = entry.split()
            inverted_index[word] = {}
            for x in xrange(1,len(data)-1):
                if(x%2 == 0):
                    continue
                else:
                    inverted_index[word][data[x]]=data[x+1]

def calculate_denominator(denominator_for_docs):
    for x in xrange(1,int(N)+1):
        denominator_for_docs['{0:04}'.format(x)] = get_den('{0:04}'.format(x))

def get_den(doc):
    sum_f = 0
    for term in inverted_index:
        if doc not in inverted_index[term]:
            continue
        else:
            idf = math.log(N/float(len(inverted_index[term])))
            temp = math.log(float(inverted_index[term][doc])) + 1
            temp = temp * idf
            temp = math.pow(temp,2)
            sum_f += temp
    sum_f = math.sqrt(sum_f)
    return sum_f

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

def load_query_frequency(query_terms):
    for term in query_terms:
        if term in query_term_frequency:
            query_term_frequency[term] += 1
        else:
            query_term_frequency[term] = 1

def calculate_query_tf_idf(query_term_frequency):
    den = get_den_q(query_term_frequency)
    for term in query_term_frequency:
        if term in inverted_index:
            idf = math.log(N/float(len(inverted_index[term])))
            num = math.log(float(query_term_frequency[term])) + 1.0
            num = num * idf
            q = num/den
            query_weights[term] = q

def get_den_q(query_term_frequency):
    sum_f = 0
    for term in query_term_frequency:
        if term in inverted_index:
            idf = math.log(N/float(len(inverted_index[term])))
            den = math.log(float(query_term_frequency[term])) + 1.0
            den = den * idf
            den = math.pow(den,2)
            sum_f += den
    return math.sqrt(den)

def calculate_tf_idf(term):
    if term in inverted_index:
        idf = math.log(N/float(len(inverted_index[term])))
        for doc in inverted_index[term]:
            num = math.log(float(inverted_index[term][doc])) + 1
            num = num * idf
            den = denominator_for_docs[doc]
            d = num/den
            if doc not in document_weigths:
                document_weigths[doc] = {}
                document_weigths[doc][term] = d
            else:
                document_weigths[doc][term] = d

def initialize_cosine_score(cosine_scores,document_weigths):
    for doc in document_weigths:
        cosine_scores[doc] = 0

def dot_product(query_weights, document_weigths):
    for doc in document_weigths:
        score = 0
        for term in query_weights:
            if term in document_weigths[doc]:
                score += query_weights[term] * document_weigths[doc][term]
        cosine_scores[doc] = score

def get_all_document_weigths(all_document_weigths):
    for term in inverted_index:
        for doc in inverted_index[term]:
            idf = math.log(N/float(len(inverted_index[term])))
            num = math.log(float(inverted_index[term][doc])) + 1
            num = num * idf
            d = num/denominator_for_docs[doc]
            if doc not in all_document_weigths:
                all_document_weigths[doc] = {}
                all_document_weigths[doc][term] = d
            else:
                all_document_weigths[doc][term] = d

def normalize_score(cosine_scores,query_weights,all_document_weigths):
    q = 0
    for doc in all_document_weigths:
        if doc not in cosine_scores:
            cosine_scores[doc] = 0
    for term in query_weights:
        temp = float(query_weights[term])
        temp = math.pow(temp,2)
        q += temp
    for doc in all_document_weigths:
        d = 0
        for term in all_document_weigths[doc]:
            temp = float(all_document_weigths[doc][term])
            temp = math.pow(temp,2)
            d += temp
        cosine_scores[doc] = cosine_scores[doc]/math.sqrt(d * q)

if __name__ == '__main__':

    load_inverted_index(inverted_index)
    calculate_denominator(denominator_for_docs)

    with open('cacm.queries.txt') as que:
        for query in que:
            document_weigths = {}
            all_document_weigths = {}
            query_weights = {}
            query_term_frequency = {}
            cosine_scores = {}
            query_terms = query.split()
            query_ID = str(query_terms[0])
            query_terms.pop(0)
            for x in xrange(len(query_terms)):
                query_terms[x] = cleanText(query_terms[x])
            load_query_frequency(query_terms)
            calculate_query_tf_idf(query_term_frequency)
            for term in query_term_frequency:
                if term in inverted_index:
                    calculate_tf_idf(term)
            initialize_cosine_score(cosine_scores,document_weigths)
            dot_product(query_weights,document_weigths)
            get_all_document_weigths(all_document_weigths)
            normalize_score(cosine_scores,query_weights,all_document_weigths)
            sort_pr = sorted(cosine_scores.items(), key=operator.itemgetter(1),reverse=True)
            f = open('cacm_queries_csvsm.txt','a')
            rank = 1
            for i in sort_pr:
                if rank <= 100: #query_id   Q0  doc_id  rank    CosineSim_score system_name
                    f.write(query_ID + ' Q0 ' + 'CACM-' +\
                    str(i[0])+' '+str(rank)+' '+str(i[1])+\
                    ' CSVSM\n')
                rank += 1
            f.close()
    que.close()
