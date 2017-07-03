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
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

#%%
# Preprocessing
#pathPaolo = "/Users/paolograniero/GitHub/RecommenderSystem/CollaborativeFiltering/"

path = "/Users/Giacomo/Google Drive/Data Science/ADM/RecommenderSystem/CollaborativeFiltering/"
#pathLivia = "/Users/livialombardi/documents/GitHub/RecommenderSystem/CollaborativeFiltering/"
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
        
    #go to dict user take user look books with higher ratings and print books not rated yet similar to the rated one
    
    def getOriginalData(self):
        """ Set the data again to the original one. The centered info is put back to False """
        self.ratings = self.originalRatings
        self.centered = False
        
        
    def similarityBooks(self,book1,book2):
        sim = 0.3*self.similarityTextFields(book1['title'],book2['title'])
        sim += 0.4*int(book1['author']==book2['author'])
        sim += 0.1*int(book1['year']==book2['year'])
        sim += 0.2*int(book1['publisher']==book2['publisher'])
        return sim
        
    
    def getSimilarBooks(self,book):
        library=self.books
        similarBooks = []
        
            
        for item in library: #scorro isbn
            similarity =  self.similarityBooks(book,library[item])
            if similarity != 1:
                similarBooks.append((item,similarity))
        return sorted(similarBooks,key=lambda x: x[1])
        
    #def topBooks(self,user):
        
 #%%       
rec = contentItemFiltering(books,ratings)
import time
start=time.time()
XSIM=rec.getSimilarBooks(rec.books['0684829746'])
print(time.time()-start)
#getSimilarBooks(self.book)
        
#%%
    def getMaxRankBooks(self,ratings):
        maxRankBooks ={}
        for users in ratings:  
            #print("### User number    :" , users)
            for item in ratings[users]:
                #print("# book    :",item)#libri
                if int(ratings[users][item])>=5:
                    if users not in maxRankBooks:
                        maxRankBooks[users] = {}
                    maxRankBooks[users][item]  = ratings[users][item]
        return maxRankBooks
    
    def simmatric(self,maxRankBooks,users):
        for book in maxRankBooks[users]:
            XSIM=getSimilarBooks(books[book])
            #pick every user in maxrank and do a recommend
            #write func to recommend
            #pock top 10 xsim books for each book read for this users
            

