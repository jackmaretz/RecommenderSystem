#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:49:01 2017

@author: paolograniero

This is the simplest possible collaborative filtering. 
It implements Manhattan distance to calculate the distance between
two users. 
Each user is an entry of a dictionary. The value associated with each
user is a dictionary containing the books with relative ratings.
The returned reccomendation is a list with the items rated by 
the closest users, sorted in descending order 
"""

#%%
import pandas as pd
import numpy as np
import json

#%%
# Read all three datasets with the correct encoding
ratings = pd.read_csv('ratings.csv', sep=';', encoding='latin1')
books = pd.read_csv('books.csv', sep=';', encoding='latin1',
                    error_bad_lines=False, warn_bad_lines=False, usecols = [0,1,2,3], 
                    index_col = 0) # removing the columns containing the links 
                    #to the images and using the ISBN column as index
users = pd.read_csv('users.csv', sep=';', encoding='latin1', error_bad_lines=False, warn_bad_lines=False)
#%%

# Drop zero ratings as they represent nothing really
ratings.drop(ratings[ratings['Book-Rating'] < 1].index, inplace=True)

#%%

# Dictionary containing all the users and relative ratings
usersRatingsDict = dict()
for ratingEntry in ratings.index:

    User_ID, ISBN, Book_Rating = ratings.loc[ratingEntry, :]
    # Some ISBN that are in ratings are not present in books. This code 
    # skips them
    # Converting this value to a string to make writing the dictionary into a 
    # json file possible
    User_ID = str(User_ID)
    Book_Rating = str(Book_Rating)
    try:
        Book_Title = books.loc[ISBN, "Book-Title"]
        if not User_ID in usersRatingsDict:
            usersRatingsDict[User_ID] = dict()
        usersRatingsDict[User_ID][Book_Title] = Book_Rating
    except:
        if not User_ID in usersRatingsDict:
            usersRatingsDict[User_ID] = dict()
        usersRatingsDict[User_ID][ISBN] = Book_Rating
#%%
with open("usersRatingsDict.json", "w") as file:
    json.dump(usersRatingsDict, file, indent = 4)

#%%

def manhattanDistance(user1, user2):
    """ Compute the manhattan distance between user1 and user2. UserX is a 
    dictionary of the form {'book1': 3, 'book2':5 ...} """
    distance = 0
    check = 0
    for book in user1:
        if book in user2:
            check = 1
            distance += abs(float(user1[book]) - float(user2[book]))
    if check == 0:
        distance = np.infty
    return distance

def computeClosestUser(userOfInterest, allUsers):
    """ Returns a sorted list of tuples containing a user and its distance from
    the userOfInterest. userOfInterest is just the str(User-ID) """
    distances = []
    for user in allUsers:
        if user != userOfInterest:
            distanceBetweenUsers = manhattanDistance(allUsers[userOfInterest], allUsers[user])
            distances.append((distanceBetweenUsers, user))
        # sort distances based on distanceBetweenUsers
    distances.sort()
    return distances
        

def recommend(userOfInterest, allUsers):
    """ Returns as recommendations the items rated by the closest user to 
    userOfInterest, selecting the ones not rated by the userOfInterest """
    # Find the closest user 
    closestUser = computeClosestUser(userOfInterest, allUsers)[0][1]
    
    recommendations = []
    
    # Find books not rated by userOfInterest
    closestUserRatings = allUsers[closestUser]
    userOfInterestRatings = allUsers[userOfInterest]
    
    for book in closestUserRatings:
        if not book in userOfInterestRatings:
            recommendations.append((closestUserRatings[book], book))
    recommendations.sort(reverse = True)
    return recommendations
    
    
