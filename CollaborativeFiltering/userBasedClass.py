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
import time
#%%
# Importing rating dictionary
ratings = json.loads(open("ratings_dict.json").read())

#%%

class collaborativeUserBased:
    
    def __init__(self, ratingsData):        # Initialize class
        self.data = copy.deepcopy(ratingsData)
        self.centered = False
        
        
    
###############################################################################
    
    def cosineSimilarity(self, user1_id, user2_id, data, cv = False):
        """ returns cosine similarity between two users, x and y, according to 
        formula cos(x,y) = sum_i(x_i*y_i)/[norm(x)*norm(y)]"""
        
        if user1_id == user2_id:
            similarity = 0
            return similarity


        """ When performing CrossValidation, looks inside the trainSimilarity 
        dictionary, that contains all the similarities between users in the complete  
        (all users considered) training set """
        if cv == True:
            try:
                similarity = float(self.trainSimilarity[user1_id][user2_id])
            except:
                similarity = float(self.trainSimilarity[user2_id][user1_id])
            return similarity
                 
            
        
            
        user1 = data[user1_id]
        user2 = data[user2_id]
        
        sumxy = 0           # Initialize the 3 terms involved in the formula
        sumx2 = 0
        sumy2 = 0
        
        for key in user1:
            
            x = float(user1[key])
            sumx2 += x**2
            
            if key in user2:
                
                y = float(user2[key])
                sumxy += x*y
                
        for key in user2:
            y = float(user2[key])
            sumy2 += y**2
        
        similarity = sumxy/(sqrt(sumx2)*sqrt(sumy2))
        
        return similarity
 
###############################################################################
    
    def k_nearest(self, user_id, data, k = 3, cv = False):
        """ Returns a list of users based on their similarity to user_id
        the elements of the list are tuples (similarity, user)"""
        
        nearest = []               # Initialize list of similarities
        for user in data:
            if user != user_id:
                similarity = self.cosineSimilarity(user_id, 
                                              user, data, cv)
                if len(nearest) == k:
                    simList = [sim for (user, sim) in nearest]
                    minimum = min(simList)
                   
                    if similarity <= minimum:
                        pass
                    else:
                        idx = simList.index(minimum)
                        nearest[idx] = (user, similarity)
                else:
                   nearest.append((user, similarity))     
        
        nearest.sort(key = lambda simTuple: simTuple[1], reverse = True)
        
        return nearest
 
##############################################################################

    def similarityData(self, data, name):
        """ Create a dictionary of similarities and save it as a json file"""
        
        simDictionary = dict()
        
        i = 0
        for user1 in data:
            simDictionary[user1] = dict()
            j = 0
            for user2 in data:
                print(i,j)
                try:
                    check = simDictionary[user2][user1]
                except:
                    simDictionary[user1][user2] = str(self.cosineSimilarity(user1, user2, data))
                j += 1
            i += 1
        
        
        filename = name + ".json"
        with open(filename, "w") as file:
            json.dump(simDictionary, file, indent= 4)

###############################################################################    

    def createTrainSet(self, completeTrain, testSet, idx):
        """ Returns the training set corresponding to a given test set, as created 
        with initializeCV() """
        
        trainSet = dict()
        
        for user in completeTrain:
            trainSet[user] = dict()
            testBooks = [book for (book, rating) in testSet[user][idx]]
            for book in completeTrain[user]:
                if not book in testBooks:
                    trainSet[user][book] = completeTrain[user][book]
        
        return trainSet
                    
###############################################################################              
        

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
        
###############################################################################        
        
    def getOriginalData(self):
        """ Set the data again to the original one. The centered info is put 
        back to False """
        self.data = self.originalData
        self.centered = False

###############################################################################

    def initializeCV(self, n_folds = 5):
        """ Create the test-sets lists to be used when performing the CV. it also  """
        if not n_folds in np.arange(5,10):
            print("Select a number of folds between 5 and 10")
            return
        self.n = n_folds
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
        
###############################################################################
        
    def recommend(self, user, data, k_nearest = 3, n_recommendations = 5, cv = False):
        """ Give a list of n_recommendations recommended (book, 
        predicted_rating) based on k_nearest neighbors according to 
        cosine similarity """
        
        #Initialize recommendations
        recommendations = dict()
        
        # Get user ratings
        userRatings = data[user]
        
        # Get nearest users
        nearest = self.k_nearest(user, data, k_nearest, cv)
        
        # Compute normalizing factor for weights
        
        normalize = 1e-12
        for nearUser in nearest:
            normalize += nearUser[1]
            
        # Iterate through all nearest users accumulating weighted 
        # ratings
        for nearUser in nearest:
            # Compute wegìight
            weight = nearUser[1]/normalize
            
            # Get Username
            username = nearUser[0]
            
            # Get dictionary of ratings for this user
            neighborRatings = data[username]
            
            # Find books rated by nearest users that user didn't
            
            for book in neighborRatings:
                if not book in userRatings:
                    
                    if not book in recommendations:
                        recommendations[book] = round(weight * float(neighborRatings[book]), 2)
                    
                    else:
                        recommendations[book] += round(weight * float(neighborRatings[book]), 2)
        
        # Convert recommendations to a list to be sorted
        recommendations = list(recommendations.items())
        
        # Sort recommendations
        recommendations.sort(key = lambda titleRating: titleRating[1], reverse = True)
        if k_nearest < 51:
            if not recommendations:
                recommendations = self.recommend(user, data, k_nearest + 1)
            
                
    
        # Return the first n_recommendations
        return recommendations[:n_recommendations]
                    
###############################################################################
                
    def CV(self, k_nearest = 3, n_recommendations = 5, max_users = np.infty):
        """ Perform n_folds CV, returning a score that represent the average percentage of successfull recommendations """
        print("K =", k_nearest, "\nn =", n_recommendations)
        scoreCV = []
        self.backup = copy.deepcopy(self.data)
        start = time.time()
        # Loop through CV rounds
        for i in np.arange(0, self.n):
            
            path = "/Users/paolograniero/Documents/AlgorithmicMethodsOfDataMining/trainData/complete"
            self.trainSimilarity = json.loads(open(path + str(i) + ".json").read())
            # Create test set
            test = dict()
            train = dict()
        
            j = 0
        
            # Build train and test set
            for user in self.testSet:
                if j > max_users:
                    break
                
                test[user] = self.testSet[user][i]
                bookTestList = [book for (book, rating) in test[user]]
                train[user] = dict()
                
                for book in self.readyForTrain[user]:
                    if not book in bookTestList:
                        train[user][book] = self.readyForTrain[user][book]
                j += 1
                
            self.data = copy.deepcopy(train)
            
            # Scoringrec
            singleScores = []
            j = len(self.data)
            z = 0
            for user in self.data:
                recommendations = self.recommend(user, self.data, k_nearest, n_recommendations, cv = True)
                recommendations = [book for (book, rating) in recommendations]
                
                bookTestList = [book for (book, rating) in test[user]]
                score = 0
                for book in recommendations:
                    if book in bookTestList:
                        score = 1
                        break
                
                #score = score / min(n_recommendations, len(bookTestList))
                singleScores.append(score)
                
                print(i, j-z, round((time.time() - start)/60, 2))
                z += 1
            scoreCV.append(np.mean(singleScores))
        
        self.data = self.backup
        return np.mean(scoreCV)
            
        
        
        
    
rec = collaborativeUserBased(ratings)
#rec.initializeCV()
#%%

users = [100, 200, 400]
K = [3, 5, 10]
N = [5, 10, 20]
scores = np.zeros((len(users), len(K), len(N)))

l = 0 
for u in users:
    m = 0
    for k in K:
        j = 0
        for n in N:
            scores[l][m][j] = rec.CV(k, n, u)
            print("Users:", u, "Nearest neighbors:", k, "# of recommendations:", n)
            j += 1
        m += 1
    l += 1
#rec.recommend('10')
