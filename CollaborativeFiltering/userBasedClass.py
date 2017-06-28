#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 22:26:14 2017

@author: paolograniero
"""
#%%
import json
from math import sqrt
import numpy as np
import copy
from random import shuffle
import matplotlib.pyplot as plt
#%%
# Importing rating dictionary
ratings = json.loads(open("ratings_dict.json").read())

#%%

class collaborativeUserBased:
    
    def __init__(self, ratingsData):        # Initialize class
        self.data = copy.deepcopy(ratingsData)
        self.centered = False
        
    def cosineSimilarity(self, user1, user2):
        """ returns cosine similarity between two users, x and y, according to formula cos(x,y) = sum_i(x_i*y_i)/[norm(x)*norm(y)]
        userX is a dictionary of the form {title:rating}"""
        
        sumxy = 0           # Initialize the 3 terms involved in the formula
        sumx2 = 0
        sumy2 = 0
        
        for key in user1:
            
            x = user1[key]
            sumx2 += x**2
            
            if key in self.data[user2]:
                
                y = user2[key]
                sumxy += x*y
                
        for key in user2:
            y = user2[key]
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
    
    def centerRatings(self):
        """ Center all the users' ratings (subtract the mean rating from 
        each one. The centered info is put to True """
        self.originalData = copy.deepcopy(self.data)
        
        for user in self.originalData:
            average_rating = np.mean([int(rating) for rating in list(self.originalData[user].values())])
            
            for book in self.originalData[user]:
                old_rating = int(self.data[user][book])
                self.data[user][book] = str(round(old_rating - average_rating, 3))
        
        self.centered = True
        
        
    def getOriginalData(self):
        """ Set the data again to the original one. The centered info is put 
        back to False """
        self.data = self.originalData
        self.centered = False

    def initializeCV(self, n_folds = 5):
        """ Create the test-sets lists to be used when performing the CV. it also  """
        self.readyForTrain = dict()
        self.testSet = dict()
        
        if self.centered == True:
            threshold = 0
        else:
            threshold = 5
            
        for user in self.data:
            if len(self.data[user]) >= n_folds:
                ratings = np.array(list(self.data[user].values()), dtype = float)
                
                if sum(ratings > threshold) >= n_folds:
                    self.readyForTrain[user] = dict()
                    self.testSet[user] = dict()

                    for book in self.data[user]:
                        rating = float(self.data[user][book])
                        if rating > threshold:
                            self.readyForTrain[user][book] = rating
                    
                    toTestSet = [(book, rating) for book, rating in zip(list(self.readyForTrain[user]), list(self.readyForTrain[user].values()))]
                       
                    shuffle(toTestSet)
                    raw_testList = np.array_split(toTestSet, n_folds)
                    # Necessary elaboration because of the way np.array_split works on tuples        
                    self.testSet[user] = [[(book, rating) for book, rating in sublist] for sublist in raw_testList]
        
        
    def recommend(self, user, k_nearest = 3, n_recommendations = 5):
        """ Give a list of n_recommendations recommended (book, 
        predicted_rating) based on k_nearest neighbors according to 
        cosine similarity """
        
                  