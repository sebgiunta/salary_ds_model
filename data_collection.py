# -*- coding: utf-8 -*-
"""
Created on Tue May 17 09:10:51 2022

@author: sebgi
"""

import glassdoor_scraper as gs
import pandas as pd

# Data Scientist

df = gs.get_jobs(10, False)

df['Salary Estimate'].value_counts()

df.to_csv('collected_data_v1.csv')


# Data Analyst

df = gs.get_jobs(1930, False)

df.to_csv('collected_data_v2.csv')


# Merge 

df_1 = pd.read_csv('collected_data_v1.csv')

df_2 = pd.read_csv('collected_data_v2.csv')

df_concat = pd.concat([df_1, df_2])

df_concat.to_csv('collected_data_merged.csv', index=False)
