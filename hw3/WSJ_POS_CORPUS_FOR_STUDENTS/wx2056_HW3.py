# This is the main progrma I write for this assignment
import pandas as pd
import nltk
import numpy as np

trainFileName = 'WSJ_02-21.pos'
testFileName = 'WSJ_24.words'
outputFileName = 'submission.pos'


tkfile = open(trainFileName,'r')
tkPOS = []
for line in tkfile.readlines():
    if line == '\n':
        tkPOS.append('Begin_Sent\tBegin_Sent\n')
    elif line == '.\t.\n':
        tkPOS.append('End_Sent\tEnd_Sent\n')
    else:
        tkPOS.append(line)
    


# Construct TABLES
likelihood = {}          # likelihood['DT'] → {'the':1500,'a':200,'an':100, …}
transition = {}          # transition['DT'] → {'NN':500,'NNP:'200,'VB':30,,…} / transition['Begin_Sent'] → {'DT':1000,'NNP':500,'VB':200, …}
word_set = set()         #All words occur in the trainning corpus

for i in range(len(tkPOS)-1):
    pair = tkPOS[i].split()          #['The', 'DT], ['Begin_Sent', 'Begin_Sent']
    token = pair[0]
    POS = pair[1]
    next_POS = tkPOS[i+1].split()[1]

    word_set.add(token)
    try:
        likelihood[POS][token] += 1
    except:
        try:
            likelihood[POS][token] = 1
        except:
            likelihood[POS] = {token:1}
    try:
        transition[POS][next_POS] += 1
    except:
        try:
            transition[POS][next_POS] = 1
        except:
            transition[POS] = {next_POS:1}

# Change from counting to frequency
for p,t in likelihood.items():
    total = 0
    for value in t.values():
        total += value
    for token in t.keys():
        likelihood[p][token] /= total
for p,next in transition.items():
    total = 0
    for value in next.values():
        total += value
    for next_key in next.keys():
        transition[p][next_key] /= total

# Check Point
print('Likelihood Checking: ',likelihood['DT'])
print('Transition Checking: ',transition['End_Sent'])

# HMM POS TAGGING MACHINE
def viterbi(sentence, L, T):     #Input: sentence = ['In', 'the', ...., 'table', '.']
    columnNum = len(sentence)+2
    rowNum = len(T)+2
    stateList = ['Begin_Sent']                                # List of all states ['DT',..., 'Begin_Sent',....]
    for state in L.keys():
        if state != 'Begin_Sent':
            stateList.append(state)
    array2D = np.zeros((rowNum, columnNum))         # Main 2D Array
    # Initializaiton
    array2D[0,0] = 1
    # Prgress
    for n in range(1,columnNum-2):    # All tokens
        for s in range(1,rowNum):   # All States
            token = sentence[n]
            productList = []                        # List of all product in cell [n,s]
            for pre_s in range(0, rowNum-2):          # Trace back to previous step
                if not token in word_set:
                    factor_1 = 1/1000               # OOV Exception: simple manipulation takes 1/1000
                else:
                    factor_1 = L[stateList[s]][token] 
                try:
                    factor_2 = T[stateList[pre_s]][stateList[s]]
                except:
                    factor_2 = 0
                factor_3 = array2D[pre_s,n-1]
                product = factor_1 * factor_2 * factor_3
                productList.append(product)
            array2D[s,n] = max(productList)         # Take the max for the cell's value
    #Choosing the path with the highest score
    path = []
    for n in range(1,columnNum-1):
        highest = 0
        tag = 0
        for s in range(1,rowNum-2):
            if array2D[s,n] >= highest:
                highest = array2D[s,n]
                tag = stateList[s]
        path.append(tag)
    return path 


# Reading Input file without tags
input = open(testFileName,'r')
token = []
tag = []
sentence = []
end_sentence = 0
for line in input.readlines():
    sentence.append(line)
    if line.strip() == ".":
        end_sentence = 1
    if end_sentence == 0:
        continue
    else:
        path = viterbi(sentence,likelihood,transition)
        token += sentence
        tag += path
        sentence = []

#  Connverging the token and generated tag
output = open(outputFileName,'w')
for i in range(len(token)):
    if token[i] != '\n':
        output.write(str(token[i]).strip()+'\t'+str(tag[i]).strip()+'\n')
    else:
        output.write(token[i])

output.close()

    

        







            







