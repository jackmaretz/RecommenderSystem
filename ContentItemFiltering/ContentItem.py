#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:55:59 2017

@author: paolograniero
"""

#%%
# Libraries
import json
import copy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

#%%
# Preprocessing
#pathPaolo = "/Users/paolograniero/GitHub/RecommenderSystem/CollaborativeFiltering/"

path = "/Users/Giacomo/Google Drive/Data Science/ADM/RecommenderSystem/CollaborativeFiltering/"

books = json.loads(open(path + "books_dict.json").read())
ratings = json.loads(open(path + "ratings_dict.json").read())
users = json.loads(open(path + "users_dict.json").read())

#%%
class contentItemFiltering:
    
    def __init__(self, booksDictionary, ratingsDictionary):
        self.books = copy.deepcopy(booksDictionary)
        self.ratings = copy.deepcopy(ratingsDictionary)
        self.centered = False
        
    def centerRatings(self):
        """ Center all the users' ratings (subtract the mean rating from 
        each one. The centered info is put to True """
        self.originalRatings = copy.deepcopy(self.ratings)
    
        for user in self.originalRatings:
            average_rating = np.mean([int(rating) for rating in list(self.originalRatings[user].values())])
        
            for book in self.originalRatings[user]:
                old_rating = int(self.ratings[user][book])
                self.ratings[user][book] = str(round(old_rating - average_rating, 3))
        
        self.centered = True

    
    def nostop_tokenizer(self,text):
        stop = stopwords.words('english')  
        tokenizer = RegexpTokenizer(r'\w+')
        return set([word.lower() for word in tokenizer.tokenize(text) if word not in stop])

    
    def jaccard(self,str1,str2):
        return len(str1.intersection(str2))/len(str1.union(str2))
        
    def similarityTextFields(self,field1,field2):
        field1Tok = self.nostop_tokenizer(field1)
        field2Tok = self.nostop_tokenizer(field2)
        return self.jaccard(field1Tok,field2Tok)
        
      
        
        
        
        
        
        
        
        
        
        


        
        
