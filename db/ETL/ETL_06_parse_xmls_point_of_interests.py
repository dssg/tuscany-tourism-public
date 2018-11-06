# coding: utf-8

# Parse xmls of points of interest
# Created by: Orsi Vasarhelyi
# Contact: orsolya.vasarhelyi@gmail.com
# Last updated: 19.07.2017.
# 
# Parse xml file given by the partner (exported from visittuscany.com) and export it to a csv

# Imports

import pandas as pd
import numpy as np 
from collections import Counter, defaultdict

#visualization
import matplotlib.pyplot as plt
import seaborn as sns

# parsing
import os
import sys
import unicodedata
import string
from collections import defaultdict
from bs4 import BeautifulSoup
import json


pathin='/mnt/data/shared/asset_geolocalizzati/'
pathout='/mnt/data/shared/'

def list_files(pathin):
    files=os.listdir(pathin)
    return files

# helper functions
def create_dict(i):
    """ parse wrongly exported xml lines as json"""
    helper_dict={}
    if len(i.find_all("arr"))>0:
        try:
            helper_dict=json.loads(i.find_all("arr")[0].get_text().strip().strip('"'))
            return helper_dict
        except:
            for el in i.find_all("arr")[0].get_text().strip().split(','):
                texts=el.strip('"').replace('{','').replace('}','').lstrip().split(":")
                helper_dict[texts[0].strip('\'')]=texts[1].strip('\'')
                return helper_dict


def create_result(info_dict,t):
    """ parse one json line into a dic"""
    results={}
    results['adress']=info_dict.get('address')
    results["lat"]=info_dict.get('lat')
    results["lng"]=info_dict.get('lng')
    if 'titolo_en' in str(i): 
        results["eng_name"]=i.select("arr[name=titolo_en]")[0].get_text().strip()
    else:
        results['eng_name']='NAN'
    if 'titolo_it' in str(i):
        results["it_name"]=i.select("arr[name=titolo_it]")[0].get_text().strip()
    else:
        results['it_name']='NAN'
    results['type']=t.split(".")[0]
    return results


def parse_all_files(files):
    """Read in all xmls from a given path, parse them and write out as a csv"""
    parsed_data=defaultdict(dict)
    j=0
    for t in files:
        with open(pathin+t) as f:
            soup = BeautifulSoup(f, "html.parser")
            docs=soup.findAll('doc')
            for i in docs[1:]:
                j+=1
                try:
                    info_dict=json.loads(i.find_all("arr")[0].get_text().strip().replace('\n',''))
                    parsed_data[j]=create_result(info_dict,t)
                except:
                    info_dict=create_dict(i) 
                    if type(info_dict)==dict and len(info_dict.keys())>0:
                        parsed_data[j]=parsed_data[j]=create_result(info_dict,t)
                    else:
                        print('xml error')

    df=pd.DataFrame.from_dict(parsed_data).T
    df.to_csv(pathout+"points_of_interest.csv")
    return df


files=list_files(pathin)
df=parse_all_files(files)
