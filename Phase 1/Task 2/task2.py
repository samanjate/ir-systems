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
    i = 0
    for entry in file_h.readlines():
        #entry = re.sub("[(,)>-]", "", entry)
        index_term = entry.split("->")
        term_list = index_term[0].split()

        term = term_list[0]
        
        inverted_index[term] = {}
        data = []
        data.append(term)
        
        args = re.sub("[(,)>-]", "", index_term[1])
        data = data + args.split()
        
        idf = math.log(3204/(len(data)-1))
        
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
            #if term == 'timesharing':
            #print(term)
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
            

def get_term_ri(query_no,term,R,sorted_score_map):
    ri = 0
    for rank in range(1,R+1):
        doc_rel = sorted_score_map[query_no][rank]
        if term in non_inverted_index[doc_rel]:
            ri += 1
    return ri
    
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

def query_score_computation(score_map,ids,avdl,R,sorted_score_map):
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
                            if len(sorted_score_map) > 0:
                                ri = float(get_term_ri(ids,q,R,sorted_score_map))
                            else:
                                ri = get_initial_ri(ids,q)
                                if ids not in relavent_documents:
                                    R = 0.0
                                else:
                                    R = float(len(relavent_documents[ids]))
                            numer = (ri+0.5)/(R-ri+0.5)
                            denom = (ni-ri+0.5)/(N-ni-R+ri+0.5)
                        
                            term_score += math.log(numer/denom)*tf_component*qf_component

                score_map[ids][doc] = term_score
        



def bm25_score_calculation(avdl,R,sorted_score_map):

    score_map = {}

    for x in range(1,len(query_map)+1):
        ids = str(x)
        score_map[ids] = {}
        query_score_computation(score_map,ids,avdl,R,sorted_score_map)
    return score_map


def sort_score_map(score_map):
    sorted_score_map = {}
    for i in range (1,len(query_map)+1):
        sorted_score_map[str(i)] = {}
        
        sorted_docs = sorted(score_map[str(i)].items(), key=operator.itemgetter(1),reverse = True)
        rank = 1
        for doc_score_tuple in sorted_docs:
            sorted_score_map[str(i)][rank] = doc_score_tuple[0]
            rank += 1
        #print("max rank: "+ str(i) +" "+str(rank))
    return sorted_score_map

def relevant_doc_terms(sorted_score_map,R):
    terms_in_rel_list = {}
    for query_no in query_map:
        terms_in_rel_list[query_no] = []
        for rank in range(1,R+1):
            doc_rel = sorted_score_map[query_no][rank]
            for term in doc_term_score[doc_rel]:
                #print(term)
                terms_in_rel_list[query_no].append(term)
    return terms_in_rel_list
        
    

def calculate_new_query_scores(sorted_score_map,R):
    alpha = 8.0
    beta = 16.0
    gamma = 4.0
    terms_in_rel_list = relevant_doc_terms(sorted_score_map,R)
    for q in range(1,len(query_map)+1):
        query_no = str(q)
        print(query_no)
        temp_query_vector = {}
        temp_query_vector[query_no] = {}
        for term in terms_in_rel_list[query_no]:
            in_query_component = alpha*float(query_map[query_no].count(term))
            summation_dij = 0.0
            for rank in range(1,R+1):
                doc_rel = sorted_score_map[query_no][rank]
                if term in doc_term_score[doc_rel]:
                    dij = doc_term_score[doc_rel][term]
                    summation_dij += dij
                
                rank += 1
            rel_doc_component = beta*(1/R)*summation_dij

            summation_dij = 0.0
            
            for rank in range(R+1,len(sorted_score_map[query_no])+1):
                doc_nonrel = sorted_score_map[query_no][rank]
                if term in doc_term_score[doc_nonrel]:
                    dij = doc_term_score[doc_nonrel][term]
                    summation_dij += dij
                rank += 1

            nonrel_docs = len(non_inverted_index) - R
            nonrel_doc_component = gamma*(1/nonrel_docs)*summation_dij

            new_query_score = in_query_component + rel_doc_component - nonrel_doc_component

            
            
            if(new_query_score > 0.0):
                temp_query_vector[query_no][term] = new_query_score
                #print(temp_query_vector)

        #print(temp_query_vector)
        sorted_term_scores = sorted(temp_query_vector[query_no].items(), key=operator.itemgetter(1),reverse = True)
        at = 0
        
        for term_score in sorted_term_scores:
            #print(str(at)+" "+term_score[0]+" "+str(term_score[1]))
            query_map[query_no].append(term_score[0])
            at += 1
            if at == 20:
                break
        
        
        
            
    

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
    
def write_results_to_file2(score_map):
    file_h = open("cacm_query_bm25_af.txt","w")
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

def load_relavtive_docs():
    with open('cacm.rel.txt') as doc_list:
        for entry in doc_list:
            words = entry.split()
            q_id = words[0]
            if q_id not in relavent_documents:
                relavent_documents[q_id] = ['{0:04}'.format(int(words[2].lstrip('CACM-')))]
            else:
                relavent_documents[q_id].append('{0:04}'.format(int(words[2].lstrip('CACM-'))))


def bm25():
    load_relavtive_docs()
    print(relavent_documents['1'])
    load_inverted_index()

    calculate_dij()
    
    #print(doc_term_score['0001'])
    
    load_queries()
    '''for q in range(1,len(query_map)+1):
        query_no = str(q)
        print(query_no+" "+str(len(query_map[query_no])))'''
        
    avdl = calculate_avdl()
    R = 0
    sorted_score_map = {}
    score_map = bm25_score_calculation(avdl,R,sorted_score_map)
    sorted_score_map = sort_score_map(score_map)
    write_results_to_file(score_map)
    #print(sorted_score_map['1'])

    #pseudo relevance - docs above rank R are assumed to be relevant
    R = 50
    calculate_new_query_scores(sorted_score_map,R)
    '''for q in range(1,len(query_map)+1):
        query_no = str(q)
        print(query_no+" "+str(len(query_map[query_no])))'''

    score_map = bm25_score_calculation(avdl,R,sorted_score_map)
    sorted_score_map = sort_score_map(score_map)
    write_results_to_file2(score_map)
    


bm25()


    


    

