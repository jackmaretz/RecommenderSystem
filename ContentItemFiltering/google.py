#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 18:16:19 2017

@author: paolograniero
"""

#%%
#import pandas as pd
import json
import requests
import time
#==============================================================================
# import csv
# import numpy as np
# from bs4 import BeautifulSoup
# import re
# from scipy.sparse import csr_matrix
# from sklearn.feature_extraction.text import TfidfVectorizer
# import sys
# from isbntools.app import *
# from collections import Counter
# from mapbox import Geocoder
# import scipy.sparse as sps
# from sklearn.feature_extraction.text import HashingVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from operator import itemgetter
# from tkinter import *
# from tkinter import filedialog
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# from PIL import Image
# from io import BytesIO
# #%%
#==============================================================================
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