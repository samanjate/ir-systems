import math
import re
import operator
import os

inverted_index ={}
dl_map = {}
query_map = {}
non_inverted_index = {}

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
    with open('inverted_index.txt') as index:
        #print(index)
        for entry in index:
            index_term = entry.split("->")
            term_list = index_term[0].split()

            term = term_list[0]
            
            inverted_index[term] = {}
            data = []
            data.append(term)
            
            args = re.sub("[(,)>-]", "", index_term[1])
            data = data + args.split()
            
            for x in range(1,len(data)-1):
                if(x%2 == 0):
                    continue
                else:
                    inverted_index[data[0]][data[x]]=data[x+1]
                make_dl_map(data[x],int(data[x+1]))
                doc = data[x]
                fik = int(data[x+1])

                if doc in non_inverted_index:
                    non_inverted_index[doc][term] = fik
                else:
                    curr = {term:fik}
                    non_inverted_index[doc] = curr

def load_queries():
    f = open("cacm_stem_temp.query.txt",'a')
    q_ID = 1
    q_string = ''
    with open("cacm_stem.query.txt") as queries:
        for query in queries:
            terms = query.split()
            f.write(str(q_ID) + ' ')
            for term in terms:
                q_string += term + ' '
            q_string = q_string.strip(' ')
            f.write(q_string + '\n')
            q_ID += 1
            q_string = ''
    f.close()

    with open("cacm_stem_temp.query.txt") as query_list:
        for query_to_be in query_list:
            query_terms = query_to_be.split()

            query_id = query_terms[0]
            query = []
            for term in query_terms[1:]:
                term = clean_text(term)
                query.append(term)
            query_map[query_id] = query

            
def get_initial_ri(query_no,term):
    ri = 0.0
    if query_no not in relavent_documents:
        return ri
    for doc_rel in relavent_documents[query_no]:
        if len(doc_rel) < 4:
            print(doc_rel)
        if term in non_inverted_index[doc_rel]:
            ri += 1.0
    return ri

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

                            ri = get_initial_ri(ids,q)
                            if ids not in relavent_documents:
                                R = 0.0
                            else:
                                R = float(len(relavent_documents[ids]))
                            numer = (ri+0.5)/(R-ri+0.5)
                            denom = (ni-ri+0.5)/(N-ni-R+ri+0.5)
                        
                            term_score += math.log(numer/denom)*tf_component*qf_component

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
            file_h.write(str(i)+" Q0 "+"CACM-"+str(doc_score_tuple[0])+" "+str(rank)+" "+str(doc_score_tuple[1])+" BM25\n")
            rank += 1

            if rank > 100:
                break
    file_h.close()

    
relavent_documents = {}

def load_relavant_docs():
    with open('cacm.rel.txt') as doc_list:
        for entry in doc_list:
            words = entry.split()
            q_id = words[0]
            if q_id not in relavent_documents:
                relavent_documents[q_id] = ['{0:04}'.format(int(words[2].lstrip('CACM-')))]
            else:
                relavent_documents[q_id].append('{0:04}'.format(int(words[2].lstrip('CACM-'))))



if __name__ == '__main__':
    load_relavant_docs()
    
    load_inverted_index()
    load_queries()

    avdl = calculate_avdl()
    
    R = 0
    sorted_score_map = {}
    score_map = bm25_score_calculation(avdl)

    write_results_to_file(score_map)
