
import re
import sys

fileName = sys.argv[1]
file =  open(fileName,'r',encoding = 'utf-8')
file_2 = open('telephone_output.txt','w')
x = file.read()
r1 = re.findall(r'\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}',x)
for r in r1:
    file_2.write(r+'\n')
    sys.stdout.write(r+'\n')
file.close()
file_2.close()
