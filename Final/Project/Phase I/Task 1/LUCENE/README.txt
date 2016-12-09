The LUCENE java program found in the IRFinalProject folder can then be run on cam.queries.txt and this gives the final result as shown in cacm_queries_lucene.

Please make sure that while running the java program, the following LOC needs to be modified according to the local computer.

1. FileInputStream fstream = new FileInputStream("/Users/samanjatesood/Documents/cacm.queries.txt");
   — this is where the input file of the program is stored, please modify the path.

2. temp = temp.replace("/Users/samanjatesood/Desktop/IR/IR-samanjate-project/cacm/CACM-", "");
   - this is where the corpus has been stored. let the “/CACM-“ part remain.

The program barely takes about 5 secs to run.