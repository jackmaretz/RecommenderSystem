#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 16:49:58 2017

@author: paolograniero
"""

#%%
import codecs
import json

path = "/Users/paolograniero/GitHub/RecommenderSystem/"

#%%
""" Creating books dictionary. Each entry is a ISBN (a dictionary itself) that 
contains title, author, year of publication and publisher"""

books = dict()

book_file = codecs.open(filename = path + "books.csv", mode = "r", encoding = "latin1")

next(book_file)
for line in book_file:
    # Separate line into fields
    fields = line.split(";")

    isbn = fields[0].strip('"')
    title = fields[1].strip('"').replace("&amp", "")
    author = fields[2].strip('"').replace("&amp", "")
    year = fields[3].strip('"')
    publisher = fields[4].strip('"').replace("&amp", "")
    books[isbn] = {"title":title, 
         "author":author, 
         "year":year, 
         "publisher":publisher}
book_file.close()

with open("books_dict.json", "w") as file:
    json.dump(books, file, indent = 4)

#%%
""" Creating user dictionary. Each entry is a User-ID (a dictionary itself) 
that contains location (state, region, province) and age """

users = dict()

user_file = codecs.open(filename = path + "users.csv", mode = "r", encoding = "latin1")

next(user_file)
for line in user_file:
    # Separate line into fields
    line = line.replace('NULL','"NULL"')
    line = line.replace("\r\n", "")
    fields = line.strip('"').split('";"')
    
    user_id = fields[0].strip('"')
    try:
        age = fields[2].strip('"')
    except:
        age = "NULL"
    
    raw_location = fields[1].strip('"').split(",")
    if (" " in raw_location or "" in raw_location):
        try:
            raw_location[raw_location.index(" ")] = "n/a"
        except:
            pass
        try:
            raw_location[raw_location.index('')] = "n/a"
        except:
            pass
    try:
        state = raw_location[2]
    except:
        state = "n/a"
    try:
        region = raw_location[1]
    except:
        region = "n/a"
        
    city = raw_location[0]
    if user_id.isdigit():
        users[user_id] = {'state':state, 
             'region':region,
             'city':city,
             'age':age}
    
user_file.close()   

with open("users_dict.json", "w") as file:
    json.dump(users, file, indent = 4)

#%%
"""Creating Ratings dictionary. Each entry is a user _id (a dictionary itself)
that contains all the rated books with the rating""" 

rating_file = codecs.open(filename = path + "ratings.csv", mode = "r", encoding = "latin1")

ratings = dict()

next(rating_file)
for line in rating_file:
    # separating line into fields
    line = line.replace("\r\n", "")
    fields = line.strip('"').split(";")
    
    user_id = fields[0].strip('"')
    isbn = fields[1].strip('"')
    rating = fields[2].strip('"')
    
    if int(rating) > 0:
        if not user_id in ratings:
            ratings[user_id] = dict()
        
   
        try:
            ratings[user_id][books[isbn]['title']] = rating
        except:
            ratings[user_id][isbn] = rating        
    
    
rating_file.close()
    
with open("ratings_dict.json", "w") as file:
    json.dump(ratings, file, indent = 4)