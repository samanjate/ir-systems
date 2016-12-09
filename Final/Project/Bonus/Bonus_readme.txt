Project 
Bonus Question
Language: Python 
Version: 2.7

Source code:-
   a. snippetgenerationg.py :- python script which takes cacm.queries.txt and results of   			       the Task1 as input i.e the file which contains the list of			       documents retrieved for each retrieval model 					       i.e(cacm_queries_bm25.txt)
   b. Input :- For each retrieval model for which we have to calculate  give one input as        	       cacm.queries.txt and other input as the result retrieved from retrieval 		       model (cacm_queries_bm25.txt) and common_words.txt represents the stop list    	       used by the algorithm.
   c. Output ::- snippet_generated.txt containing the snippets generated for the given set 		of queries for the given retrieval model

Thing to modify for running on multiple files:-

a. For running the script for other retrieval methods change the path to the new results file as retrieved from the task1 (i.e the file containing the list of document retrieved by a given retrieval model for a given set of queries).