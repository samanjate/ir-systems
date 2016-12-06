To run LUCENE on the given queries in file cacm.query.txt, we first run a python script to 
convert it into a readable format by the java program. 

The Script.py takes calm.query.txt as inept and then gives calm.queries.txt file.

The LUCENE java program found in the IRFinalProject folder can then be run on cam.queries.txt 
and this gives the final result as shown in cacm_queries_lucene.

Please make sure that while running the java program, the following LOC need to be modified 
according to the local computer.

1. FileInputStream fstream = new FileInputStream("/Users/samanjatesood/Documents/cacm.queries.txt");
   — this is where the input file of the program is stored, please modify the path.

2. temp = temp.replace("/Users/samanjatesood/Desktop/IR/IR-samanjate-project/cacm/CACM-", "");
   - this is where the corpus has been stored. let the “/CACM-“ part remain.