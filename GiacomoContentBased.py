import pandas as pd
import numpy as np
import nltk
import time
import redis
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import itertools


#loading dataframe
books= pd.read_csv('books.csv',delimiter=';',encoding='latin1',error_bad_lines=False, warn_bad_lines=False,low_memory=False) #load books file, dropping bad rows;

#cleaning dataframe
column_to_delete=list(books.columns.values)[5:8]
books= books.drop(labels=column_to_delete, axis=1) # axis 1 drops columns, 0 will drop rows that match index value in labels
#print(books.iloc[128880:128899,:])



#dictionary
dict = {}
i=1
start = time.time()

# for id, book in books.iterrows():
#
#     #print(i)
#     isbn, title, author, year, publisher = book
#     publisher = "" if type(publisher) == float else publisher
#     pub=nltk.word_tokenize(publisher)
#     dict[isbn]= {'Title': nltk.word_tokenize(title), 'Author' : nltk.word_tokenize(author),'Year' : nltk.word_tokenize(year), 'Publisher': pub}
#     i=i+1
description=[]
id=[]
i=0
for ident, book in books.iterrows():

    print(i)
    isbn, title, author, year, publisher = book
    publisher = "" if type(publisher) == float else publisher
    description.append(title+author+year+publisher)
    id.append(isbn)

    i=i+1

# for id, book in books.iterrows():
#     isbn, title, author, year, publisher = book
#     ISBN.append(isbn)
#     TOKENS.append(nltk.word_tokenize(title)+ nltk.word_tokenize(author)+nltk.word_tokenize(year)+ nltk.word_tokenize(publisher))
#     print(i)
#     i=i+1
#     break
#df=pd.DataFrame(columns=(ISBN,TOKENS))

print("Engine trained in %s seconds." % (time.time() - start))

#print(books.head())
#data=pd.DataFrame()

#df=pd.DataFrame(np.column_stack([id, description]),columns=(id,description))
#print(df.head())
d=pd.DataFrame(
    {'id': id,
     'description': description,
    })
print(d.head())
d.set_index('id', inplace=True)

print(d.head())


#1.tokenize words in dictionary
#2.stemm them
#3.find similarity between each field
#4.get total similarity by summing all similarities
#5.print top k most similar books

#PART FOUND ONLINE
"""
        Train the engine.
        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product. The 'stop_words' param
        tells the TF-IDF module to ignore common english words like 'the', etc.
        Then we compute similarity between all products using SciKit Leanr's linear_kernel (which in this case is
        equivalent to cosine similarity).
        Iterate through each item's similar items and store the 100 most-similar. Stops at 100 because well...
        how many similar products do you really need to show?
        Similarities and their scores are stored in redis as a Sorted Set, with one set for each item.
        :param ds: A pandas dataset containing two fields: description & id
        :return: Nothin!
        """

ds=d
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds[''])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

    # First item is the item itself, so remove it.
    # This 'sum' is turns a list of tuples into a single tuple: [(1,2), (3,4)] -> (1,2,3,4)
    flattened = sum(similar_items[1:], ())
    #self._r.zadd(self.SIMKEY % row['id'], *flattened)
print(flattened)
print(cosine_similarities)
print(tfidf_matrix)