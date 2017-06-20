#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 23:05:48 2017

@author: paolograniero

This is a simple content-based recommender system. We take into account author, publisher and year of publication of the books to buil item and user profile. The input is a text file containing just ISBN, one per line. The program calculate the cosine similarity between the user vector and item vector. Actually we don't build the item and user vectors, instead we exploit the fact that in the dot product only the features that are present both in the user vector and in the item one come into play, so we can just check for equality of each feature in the book database and rearrange the operations of dot product in this way. Because each item vector is boolean and has just three nonzero component, it is also unnecessary to divide by the product of the norms (it's the same for all vectors)  
"""


import pandas as pd
import numpy as np

books = pd.read_csv('books.csv', index_col = 0, dtype = 'object') # Read the database obtained converting the original one to a tab separated file with R, dtype to solve a problem with the Year-Of-Publication: a number cannot be compared with strings
books.index = books.ISBN
book_show = books.loc[:,['Book-Title','Book-Author','Year-Of-Publication','Publisher']] # The database utilised to show the recommended books (include also the titles of the books
books = books.loc[:,['Book-Author','Year-Of-Publication','Publisher']] # Selecting only the features of interest to construct the item profiles
books.dropna(axis = 0, inplace = True) # Removing lines with 'problems', that shows na's
book_show.dropna(axis = 0, inplace = True)
#%%
user = list(pd.read_table('user.txt', header = None, dtype = 'object')[0]) # Transforming the DataFrame obtained with pd.read_table to a pandas Series, that is convertible in a list
v_user = [] # List that collect the features of the books contained in user
for isbn in user:               # collect all the features of interest of the books whose ISBN is in the user file
    v_user.extend(list(books.loc[isbn, :].values))
books.drop(labels = user, axis = 0, inplace = True) # Remove the entries corresponding to the books in user to avoid recommending books already read
book_show.drop(labels = user, axis = 0, inplace = True)
#%%
dist = np.zeros(shape = len(books)) # Initializing the distance vector
for feat in v_user:
    try:
        dist += (books == feat).sum(axis = 1).values # Expoloit what mentioned in the description of the script regarding the features that come into play in the dot product involved in the computation of cosine similarity
    except:
        pass        # In case there are unmatched features
dist = dist/(len(v_user)*3)

print(book_show.iloc[np.argsort(dist)[-5:], :]) # Shows the first 5 most recommended books as a DataFrame extracted from book_show
