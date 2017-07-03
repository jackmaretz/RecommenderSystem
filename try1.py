#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 20:10:23 2017

@author: Giacomo
"""

for user in ratings:
    for i in users:
        if int(i[1]) >= 5:
            print(ratings[user][i])
    