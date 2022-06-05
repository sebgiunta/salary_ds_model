# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 16:00:34 2022

@author: sebgi
"""

import pandas as pd

df = pd.read_csv('datasets/collected_data_merged.csv', index_col=0)

#salary parsing
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if '/hr' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('/')[0])
alter_salary = salary.apply(lambda x: x.replace(',','').replace('$',''))
alter_salary = alter_salary.astype('float')
final_salary = alter_salary.apply(lambda x: x*2080 if x < 500 else x)

df['salary'] = final_salary

#company name text only
df['company_txt'] = df.apply(lambda x: x['Company Name'][:-3], axis=1)

#age of company
df['age'] = df.Founded.apply(lambda x: x if x<1 else 2022-x)

#parsing of job description (python, etc.)
#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

#aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

#excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

#communication
df['communication_yn'] = df['Job Description'].apply(lambda x: 1 if 'communication' in x.lower() else 0)


#df.to_csv('salary_data_cleaned.csv', index=False)
