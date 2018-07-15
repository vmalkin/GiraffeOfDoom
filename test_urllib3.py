#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 11:55:44 2018

@author: vaughn
"""

import urllib3

http = urllib3.PoolManager()
# r = http.request('GET', 'http://httpbin.org/robots.txt')

response = http.request("GET", "http://www.ruruobservatory.org.nz/dr01_1hr.csv")

for item in response.data:
    print(item)
