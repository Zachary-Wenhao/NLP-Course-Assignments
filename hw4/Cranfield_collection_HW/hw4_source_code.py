closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]
import math
from nltk.stem import PorterStemmer
ps = PorterStemmer()  # Word Stemming using NLTK

# Files
queryFileName = "cran.qry"
collectionFileName = 'cran.all.1400'
outputFileName = 'output.txt'

# PART 1
# Data Pre-pocessing of QUERYS
querys = open(queryFileName,'r')
query_list = list(querys)
query_dic = {}
count = 0
load = 0
for i in range(len(query_list)):
  if query_list[i][0:2] == '.I':
    count += 1
    load = 0
    query_dic[count] = ""
  elif query_list[i][0:2] == '.W':
    load = 1
  elif load:
    query_dic[count] += query_list[i]
print("Raw Querys-----------------------------------------------------------")
print(query_dic)
  
for key in query_dic.keys():
  query_dic[key] = query_dic[key].split()
print("Querys After Spliting-------------------------------------------------------")
print(query_dic)

for key in query_dic.keys():
  new_list = []
  for word in query_dic[key]:
    if (word not in closed_class_stop_words) and (word.isalpha()):
      new_list.append(ps.stem(word))
  query_dic[key] = new_list
print("Querys After Removing Stop List Words------------------------------------")
print(query_dic)
print('Length Check:'+ str(len(query_dic)))



# Data Pre-pocessing of DOC COLLECTION
collection = open(collectionFileName,'r')
collection_list = list(collection)
collection_dic = {}
load_2 = 0
count_2 = 0
for i in range(len(collection_list)):
  if collection_list[i][0:2] == '.I':
    count_2 += 1
    load_2 = 0
    collection_dic[count_2] = ''
  elif collection_list[i][0:2] == '.W':
    load_2 = 1
  elif load_2:
    collection_dic[count_2] += collection_list[i]
print("Collection with only Num and Abstract------------------------------------")
# print(collection_dic)

for key in collection_dic.keys():
  collection_dic[key] = collection_dic[key].split()
print("Collection After Spliting-------------------------------------------------------")
# print(collection_dic)

for key in collection_dic.keys():
  new_list = []
  for word in collection_dic[key]:
    if (word not in closed_class_stop_words) and (word.isalpha()):
      new_list.append(ps.stem(word))
  collection_dic[key] = new_list
print("Colleciton After Removing Stop List Words------------------------------------")
print('Length Check:'+ str(len(collection_dic)))


# PART 2
# IDF of words in all queries
IDF_queries = {}
total_queries = len(query_dic)+1  
for val in query_dic.values():
  for word in val:
    if word not in IDF_queries:
      count = 1
      for q in query_dic.values():
        if word in q:
          count += 1
      IDF_queries[word] = math.log(total_queries/count)         # Calculate IDF scores for each word in the collection of queries
    else:
      continue

# feature vector of all queries
featured_vectors = {}
for i in query_dic.keys():
  featured_vectors[i] = []
  for word in query_dic[i]:
    term = query_dic[i].count(word) / len(query_dic[i])           # Count the number of instances of each non-stop-word in each query
    TF = math.log((term+1)/(len(query_dic[i])+1))   
    IDF = IDF_queries[word]
    TFIDF = TF * IDF 
    featured_vectors[i].append(TFIDF)
print('Check feature Vectors of queries no.1: ', featured_vectors[1])

# Cosine Similarity Function
def CosSim(l1,l2):
  if len(l1) != len(l2):
    raise ValueError("Two vectors' lenghts don't match!")
  if len(l1) == 0 or len(l2) == 0:
    raise ValueError('Empty Vectors!')
  numor, a_seq_sum, b_seq_sum= 0,0,0
  for i in range(len(l1)):
    numor += (l1[i] * l2[i])
    a_seq_sum += (l1[i] ** 2)
    b_seq_sum += (l2[i] ** 2)
  if a_seq_sum == 0 or b_seq_sum == 0:
    return 0
  else:
    return (numor / math.sqrt(a_seq_sum * b_seq_sum))
print("Function Check: ",CosSim([0,5,0,5,0],[0,7,0,9,0]))

# IDF of words in the collection of abstracts
IDF_abstract= {}
total_abstract = len(collection_dic)+1  
for val in collection_dic.values():
  for word in val:
    if word not in IDF_abstract:
      count = 1
      for q in collection_dic.values():
        if word in q:
          count += 1
      IDF_abstract[word] = math.log(total_abstract/count)
    else:
      continue

# Main Loop
main_dic = {}                   # { query_1:{ abstract_1:2, abstract_2:-1, ...} }
for q in query_dic.keys():      # For each query  
  main_dic[q] = {}
  for a in collection_dic.keys():  # For each abstract
    abstract_vector = []       
    for w in query_dic[q]:
      if w in collection_dic[a]:
        term = collection_dic[a].count(w) / len(collection_dic[a])
        TF = math.log((term+1)/(len(collection_dic[a])+1))  
        IDF = IDF_abstract[w]
        TFIDF = TF * IDF
        abstract_vector.append(TFIDF)
      else:
        abstract_vector.append(0)
    # Cosine Sim for each abstract
    sim_score = CosSim(featured_vectors[q], abstract_vector)
    main_dic[q][a] = sim_score


# Sort Cosine Similarity
for q in main_dic.keys():
  sort = sorted(main_dic[q].items(), key=lambda x: x[1], reverse = True)
  main_dic[q] = sort

# elimination
for q in main_dic.keys():
  new_list = []
  for a in main_dic[q]:
    if a[1] >= 0.4:
      new_list.append(a)
  if len(new_list) >= 100:
    main_dic[q] = new_list
    
# Output File
output = open(outputFileName,'w')
for q in main_dic.keys():
  for a in main_dic[q]:
    query_num = q
    abstract_num = a[0]
    score = a[1]
    output.write(str(query_num)+' '+str(abstract_num)+' '+str(score)+'\n')

output.close()