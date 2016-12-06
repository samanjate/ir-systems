import re
import operator

q_IDs = []
q_text = []
text = ''
queries = {}

with open('cacm.query.txt') as rawfile:
    for line in rawfile:
        if '</DOC>' in line:
            q_text.append(text)
            text = ''
            continue
        if '<DOC>' in line:
            continue
        if '<DOCNO>' in line:
            q_IDs.append(line)
            continue
        else:
            text += line

for x in xrange(len(q_IDs)):
    q_IDs[x] = int(q_IDs[x].split()[1])

for x in xrange(len(q_text)):
    temp = q_text[x].splitlines()
    temp_text = ''
    for y in xrange(len(temp)):
        temp_text += temp[y] + ' '
    q_text[x] = temp_text.strip(' ')
    q_text[x] = re.sub(' +',' ',q_text[x])

for x in xrange(len(q_IDs)):
    queries[q_IDs[x]] = q_text[x]

sort_pr = sorted(queries.items(), key=operator.itemgetter(0))
program_input = open('cacm.queries.txt','w')
for i in sort_pr:
    program_input.write(str(i[0])+ " " + str(i[1]) +'\n')
program_input.close()
