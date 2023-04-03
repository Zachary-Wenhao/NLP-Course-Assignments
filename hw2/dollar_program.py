import re
import sys

fileName = sys.argv[1]
file = open(fileName,'r',encoding = 'utf-8')
x = file.read()
rl = re.findall(r'\$*[A-Za-z0-9.,]+\s+millions?|\$*[A-Za-z0-9.,]+\s+billions?|[A-Za-z0-9.,]+\s+dollars?\s+and\s+[A-Za-z0-9.,]+\s+cents?|\$*[A-Za-z0-9.,]+\s+thousand\s+dollars?|\$*[A-Za-z0-9.,]+\s+hundred\s+thousand\s+dollars?|\$*[A-Za-z0-9.,]+\s+dollars?|\$*[A-Za-z0-9.,]+\s+cents?|\$[A-Za-z0-9.,]+',x)

file_2 = open('dollar_output.txt',"w")
for r in rl:
    if ("the " in r) or ("in " in r) or ("per "in r) or ("th " in r):
        continue
    l = len(r)
    if r[l-1] == '.':
        r = r[:l-1]
    file_2.write(r+'\n')
    sys.stdout.write(r+"\n")
file.close()
file_2.close()


