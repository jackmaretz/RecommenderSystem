import pandas as pd
import numpy as np
import nltk

#loading dataframe
books= pd.read_csv('books.csv',delimiter=';',encoding='latin1',error_bad_lines=False, warn_bad_lines=False,low_memory=False) #load books file, dropping bad rows;

#cleaning dataframe
column_to_delete=list(books.columns.values)[5:8]
books= books.drop(labels=column_to_delete, axis=1) # axis 1 drops columns, 0 will drop rows that match index value in labels
#print(books.iloc[128880:128899,:])

#dictionary
dict = {}
i=1
for id, book in books.iterrows():
    #print(i)
    isbn, title, author, year, publisher = book
    publisher = "" if type(publisher) == float else publisher
    pub=nltk.word_tokenize(publisher)
    dict[isbn]= {'Title': nltk.word_tokenize(title), 'Author' : nltk.word_tokenize(author),'Year' : nltk.word_tokenize(year), 'Publisher': pub}
    i=i+1

#1.tokenize words in dictionary
#2.stemm them
#3.find similarity between each field
#4.get total similarity by summing all similarities
#5.print top k most similar books