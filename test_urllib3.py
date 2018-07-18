#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 11:55:44 2018
@author: vaughn
"""
import urllib3
# import certifi

##########################################################
# Function to pass on data from a URL
##########################################################
def get_url_data(url_string):
    # http = urllib3.PoolManager(cert_reqs = "cert_required", ca_certs=certifi.where())
    http = urllib3.PoolManager()
    data_list = []
ium for w        
    try:
        response = http.request("GET", url_string)
        # get the repsonse data, convert to UTF-8 and split on the carriage returns
        text = response.data.decode("utf-8").splitlines()
        
        # Create a list from the text data
        for item in text:
            item.strip("\n")
            data_list.append(item)
    
        # delete header row 
        data_list.pop(0)
    except urllib3.exceptions.HTTPError:
        print("Error with URL")
        
    return data_list



if __name__ == "__main__":
    urlvalue = "http://www.ruruobservatory.org.nz/dr01_1hr.csv"
    csv_data = get_url_data(urlvalue)

