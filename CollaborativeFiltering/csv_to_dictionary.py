#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 16:49:58 2017

@author: paolograniero
"""

#%%
import codecs
import json
import requests
import time

path = "/Users/paolograniero/GitHub/RecommenderSystem/"

def get_goog_description(isbn):
    lapi_key = '&key=AIzaSyDOujjCI2UI6LqoL44wwPgXQpVOgJLPp2g' #api key;
    base_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' #endpoint;
    description = ''

    status_code = 0 #this is the status of the request;
    tries = 0 #this is the number of times we tried requesting page;
    while(status_code != 200 and tries < 5): #try requesting until ok response;     
        try:
            content = requests.get(base_url + isbn, timeout=10) #request page;
            status_code = content.status_code #get status code of request;
        except Exception as RequestError:
            print(RequestError)
            status_code = 502        
        time.sleep(1) #wait for 1 second;
        tries += 1 #increment tries;
    if (status_code == 200): #response ok;
        json_book = json.loads(content.text) #load returned json object;
        try:
            description = json_book['items'][0]['volumeInfo']['description'].lower() #try fetching the description from the json object;
        except Exception as e:
            pass
    return description
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
    # description = get_goog_description(isbn)
    if isbn in isbnSet:
        books[isbn] = {"title":title, 
         "author":author, 
         "year":year, 
         "publisher":publisher} #,
         #"description": description}
book_file.close()

with open("books_dict_cut.json", "w") as file:
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
isbnSet = []
user_idSet = []
next(rating_file)
i = 1
for line in rating_file:
    
    if i > 100:
        break
    
    # separating line into fields
    line = line.replace("\r\n", "")
    fields = line.strip('"').split(";")
    
    user_id = fields[0].strip('"')
    isbn = fields[1].strip('"')
    rating = fields[2].strip('"')
    
    if int(rating) > 0:
        i += 1
        isbnSet.append(isbn)
        user_idSet.append(user_id)
        if not user_id in ratings:
            ratings[user_id] = dict()
        
   
        try:
            ratings[user_id][books[isbn]['title']] = rating
        except:
            ratings[user_id][isbn] = rating        
    
    
    
    
rating_file.close()
print(len(isbnSet))
isbnSet = set(isbnSet)
print(len(isbnSet))
user_idSet = set(user_idSet)
with open("ratings_dict_cut.json", "w") as file:
    json.dump(ratings, file, indent = 4)