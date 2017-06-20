#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:23:24 2017

@author: aydanselek
"""
import pandas as pd
#%%
# Load Users
users_pd=pd.read_csv('BX-Users.csv', delimiter=';', encoding='latin1', error_bad_lines=False)
#%%
# Load Books
names=["ISBN","Book-Autor", "Year-Of-Publication","Publisher"]
books_pd=pd.read_csv('BX-Books.csv', delimiter=';', encoding='latin1', error_bad_lines=False, warn_bad_lines=False, low_memory=False )

#drop var we dont want
books_pd.drop(['Image-URL-S','Image-URL-M','Image-URL-L','Book-Title'],axis=1,inplace=True)
#%%
# Load Ratings
ratings_pd=pd.read_csv('BX-Book-Ratings.csv',delimiter=';',encoding='latin1',error_bad_lines=False)
#%%
# Merge all in one table
all_pd = pd.merge(pd.merge(users_pd, ratings_pd, on='User-ID', how='inner'), books_pd[['ISBN','Book-Author','Year-Of-Publication','Publisher']], on='ISBN', how='inner')
#all_pd['Year-Of-Publication'] = all_pd['Year-Of-Publication'].apply(pd.to_numeric, errors='coerce')
#%%

