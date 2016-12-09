Project 
Phase2: 
Language: Python 
Version: 2.7

Source code:-
   a. mrr.py :- python script which takes cacm.txt and results of the Task1 as input 		i.e the file which contains the list of documents retrieved for each retrieval 		model i.e(cacm_queries_tfidf)
   b. Input :- For each retrieval model for which we have to calculate MAP, 	     		       MRR ,Precision,Recall give one input as cacm.txt and other input as
	       the result retrieved from retrieval model (cacm_queries_tfidf.txt)
   c. Output :- 1. MRRtfidf.txt :- a.containing the MAP for this retrieval model
				   b.MRR for the this retrieval model
				   c.Precision at rank 5 and 20 for all the queries.
		2.precision_dict_cacm_queries_tfidf.csv : Containing the precision for
				   for all the queries till 100 ranks.
		3.recall_dict_cacm_queries_tfidf.csv : Containing the recall for
				   for all the queries till 100 ranks.

Thing to modify for running on multiple files:-

a. For running the script for other retrieval methods change the path to the new results file as retrieved from the task1 (i.e the file containing the list of document retrieved by a given retrieval model for a given set of queries). line no. 97 in code
