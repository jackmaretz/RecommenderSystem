#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 11:47:58 2017

@author: paolograniero
"""
#%%

import pandas as pd
import numpy as np
from collections import Counter
import re
from scipy.spatial.distance import cosine

def import_books(path = 'BX-Books.csv'):
    
    file = open(path, encoding = 'ISO-8859-1')
    lines=[]
    for row in file:
        lines.append(re.split('";"', row))
        
    df = []
    for line in lines:
        s = []
        for word in line:
            s.append(re.sub('"', '', word))
        df.append(s)
        
    values = np.array(df[1:])
    dataset = pd.DataFrame(columns = df[0], data = values)
    return dataset

booksRatings = pd.read_csv('BX-Book-Ratings.csv', index_col = 0, header = 0, encoding = 'ISO-8859-1', sep = ';', dtype = 'O')
#%%

booksRatings.replace(to_replace = {'Book-Rating' : { '0': 1,'1':1, '2':1, '3':2, '4':2, '5':3, '6':3, '7':4, '8':4, '9':5, '10':5}}, inplace = True)



countUsers = Counter(booksRatings.index)
activeUsers = [x for (x,y) in countUsers.items() if y > 100]
inactiveUsers = [x for (x,y) in countUsers.items() if y <= 100]

booksRatings.drop(labels = inactiveUsers, axis = 0, inplace = True)



utilityMatrix = pd.pivot(index = booksRatings.index, columns = booksRatings.ISBN, values = booksRatings['Book-Rating'])

(utilityMatrix.sum(axis = 1) == 0).sum()

#%%
def cosSimMat(utilityMatrix):
    centered = utilityMatrix.values - utilityMatrix.mean(axis = 1).values.reshape(-1,1)
    centered = np.nan_to_num(centered)
    
    n = len(centered)
    cosMatr = np.zeros((n,n))
    for i in range(0,n-1):
        u = centered[i,:]
        for j in range(i+1, n):
            v = centered[j,:]
            cosMatr[i,j] = 1 - cosine(u,v)
        print(n-i)
    return cosMatr

coSimMatrix = cosSimMat(utilityMatrix)
#%%

from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

centeredT = centered.transpose
centered_sparse = sparse.csr_matrix(centeredT)

similarities = cosine_similarity(centered_sparse)
