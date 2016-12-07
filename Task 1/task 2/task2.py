import math
import re
import operator

inverted_index ={}
dl_map = {}
query_map = {}

score_square_denom = {}
non_inverted_index = {}
doc_term_score = {}

k1 = 1.2
k2 = 100.0
b = 0.75

def make_dl_map(doc,freq):
    if doc in dl_map:
        dl_map[doc] += freq
    else:
        dl_map[doc] = freq

def calculate_avdl():
    total = 0
    for doc in dl_map:
        total += dl_map[doc]
        
    avdl = total/len(dl_map)
    return avdl

def calculate_k(doc,avdl):
    
    k = k1*((1-b) + (b*(dl_map[doc]/avdl)))
    return k

def clean_text(text):
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

def load_inverted_index():
    file_h = open("inverted_index.txt","r")
    #print(len(file_h.readlines()))
    for entry in file_h.readlines():
        entry = re.sub("[(,)>-]", "", entry)
        data = entry.split()
        inverted_index[data[0]] = {}

        term = data[0]
        idf = math.log(3204/len(data))
        
        for x in range(1,len(data)):
            if(x%2 == 0):
                continue
            else:
                inverted_index[data[0]][data[x]]=data[x+1]
            make_dl_map(data[x],int(data[x+1]))
            doc = data[x]
            fik = int(data[x+1])
            
            #term weight denominator calculation 
            norm_denom = math.pow(((math.log(fik) + 1) * idf),2)
            if doc in score_square_denom:
                score_square_denom [doc] += norm_denom
            else:
                score_square_denom[doc] = norm_denom

            #make a non-inverted index
            if doc in non_inverted_index:
                non_inverted_index[doc][term] = fik
            else:
                curr = {term:fik}
                non_inverted_index[doc] = curr


def calculate_dij():
    for doc in non_inverted_index:
        doc_term_score[doc] = {}
        for term in non_inverted_index[doc]:
            idf = math.log(3204/len(inverted_index[term]))
            fik = float(non_inverted_index[doc][term])
            score_numer = (math.log(fik) + 1) * idf
            score = score_numer/math.sqrt(score_square_denom[doc])

            doc_term_score[doc][term] = score
            

def load_queries():
    with open("cacm.queries.txt") as query_list:
        for query_to_be in query_list:
            query_terms = query_to_be.split()

            query_id = query_terms[0]
            query = []
            for term in query_terms[1:]:
                term = clean_text(term)
                query.append(term)
            query_map[query_id] = query


def query_score_computation(score_map,ids,avdl):
    N = len(dl_map)
    # for each term in a query
    for term in query_map[ids]:
        #if the term is in the index
        if term in inverted_index:
            #for each document having the term
            for doc in inverted_index[term]:
                term_score = 0
                #calculate query score for entire query
                for q in query_map[ids]:
                    #if query term is not in index
                    if q in inverted_index:
                        ni = len(inverted_index[q])

                        if doc in inverted_index[q]:
                            fi = float(inverted_index[q][doc])
                            
                            tf_component = ((k1 + 1) * fi)/(calculate_k(doc,avdl) + fi)

                            qfi = float(query_map[ids].count(q))
                            qf_component = ((k2 + 1) * qfi)/(k2+qfi)

                            term_score += math.log((1/((ni+0.5)/(N-ni+0.5)))*tf_component*qf_component)

                score_map[ids][doc] = term_score
    



def bm25_score_calculation(avdl):

    score_map = {}

    for x in range(1,len(query_map)+1):
        ids = str(x)
        score_map[ids] = {}
        query_score_computation(score_map,ids,avdl)
    return score_map


def write_results_to_file(score_map):
    file_h = open("cacm_query_bm25.txt","w")
    for i in range (1,len(query_map)+1):
        sorted_docs = sorted(score_map[str(i)].items(), key=operator.itemgetter(1),reverse = True)

        rank = 1

        for doc_score_tuple in sorted_docs:
            file_h.write(str(i)+" Q0 "+str(doc_score_tuple[0])+" "+str(rank)+" "+str(doc_score_tuple[1])+" BM25\n")
            rank += 1

            if rank > 100:
                break
    file_h.close()
    

def bm25():
    load_inverted_index()

    calculate_dij()
    print(doc_term_score['0001'])
    
    load_queries()

    avdl = calculate_avdl()
    
    score_map = bm25_score_calculation(avdl)

    write_results_to_file(score_map)


bm25()


    


    

