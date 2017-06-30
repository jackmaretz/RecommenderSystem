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
#%%
# Preprocessing
path = "/Users/paolograniero/GitHub/RecommenderSystem/CollaborativeFiltering/"

books = json.loads(open(path + "books_dict.json").read())

users = json.loads(open(path + "users_dict.json").read())

def jaccard(s1,s2):
    return len(s1.intersection(s2))/len(s1.union(s2))


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


    def bagOfWords(self, field):
        
