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

#%%
# Read all three datasets with the correct encoding
ratings = pd.read_csv('ratings.csv', sep=';', encoding='latin1')
books = pd.read_csv('books.csv', sep=';', encoding='latin1',
                    error_bad_lines=False, warn_bad_lines=False, usecols = [0,1,2,3], 
                    index_col = 0) # removing the columns containing the links 
                    #to the images and using the ISBN column as index
users = pd.read_csv('users.csv', sep=';', encoding='latin1', error_bad_lines=False, warn_bad_lines=False)
#%%

## Drop zero ratings as they represent nothing really
# ratings.drop(ratings[ratings['Book-Rating'] < 1].index, inplace=True)

#%%

# Dictionary containing all the users and relative ratings
usersRatingsDict = dict()
for ratingEntry in ratings.index:

    User_ID, ISBN, Book_Rating = ratings.loc[ratingEntry, :]
    # Some ISBN that are in ratings are not present in books. This code 
    # skips them
    try:
        Book_Title = books.loc[ISBN, "Book-Title"]
        if not User_ID in usersRatingsDict:
            usersRatingsDict[User_ID] = dict()
        usersRatingsDict[User_ID][Book_Title] = Book_Rating
    except:
        if not User_ID in usersRatingsDict:
            usersRatingsDict[User_ID] = dict()
        usersRatingsDict[User_ID][ISBN] = Book_Rating
    
# Calculate the number of users that gave no rating
usersSet = set(users["User-ID"])
ratingsSet = set(ratings["User-ID"])
nonRatingUsers = len(usersSet.difference(ratingsSet))
