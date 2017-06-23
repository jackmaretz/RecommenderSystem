#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 22:26:14 2017

@author: paolograniero
"""
#%%
import json
from math import sqrt
#%%
# Importing rating dictionary
ratings = json.loads(open("ratings_dict.json").read())

#%%

class collaborativeUserBased:
    
    def __init__(self, ratingsData):        # Initialize class
        self.data = ratingsData
        
    def cosineSimilarity(self, user1, user2):
        """ returns cosine similarity between two users, x and y, according to formula cos(x,y) = sum_i(x_i*y_i)/[norm(x)*norm(y)]
        userX is a dictionary of the form {title:rating}"""
        
        sumxy = 0           # Initialize the 3 terms involved in the formula
        sumx2 = 0
        sumy2 = 0
        
        for key in user1:
            if key in self.data[user2]:
                
                x = user1[key]
                y = user2[key]
                
                sumxy += x*y
                sumx2 += x**2
                sumy2 += y**2
        
        similarity = sumxy/(sqrt(sumx2)*sqrt(sumy2))
        
        return similarity
    
    def k_nearest(self, user_id, k = 3):
        """ Returns a list of users based on their similarity to user_id
        the elements of the list are tuples (similarity, user)"""
        
        sims = []               # Initialize list of similarities
        for user in self.data:
            if user != user_id:
                similarity = cosineSimilarity(self.data[user_id], 
                                              self.data[user])
                sims.append((user, similarity))
        
        sims.sort(key = lambda simTuple: simtuple[1], reverse = True)
        
        return sims[:k]
    
    
    
            
        