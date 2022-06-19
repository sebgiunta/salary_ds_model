# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 08:31:40 2022

@author: sebgi
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error

import statsmodels.api as sm



df = pd.read_csv('datasets/salary_data_cleaned.csv')

# Choose relevant columns
df.columns

df_model = df[['Rating', 'Size', 'Type of ownership', 'Industry',
             'Sector', 'Revenue', 'hourly', 'salary', 'age', 'python_yn', 
             'aws_yn','excel_yn', 'communication_yn', 'job_title', 'seniority', 
             'desc_len']]

# Get dummy data
df_dum = pd.get_dummies(df_model, drop_first=True)


# train test split
X = df_dum.drop('salary', axis=1)
y = df_dum['salary'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Multiple Linear Regression

X_sm = sm.add_constant(X)
model = sm.OLS(y, X_sm)
model.fit().summary()


lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))


# Lasso Regression
lm_l = Lasso()
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))

alpha = []
error = []

for i in range(1,200):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))
    
plt.plot(alpha,error)

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]

# Random Forest
rf = RandomForestRegressor()

np.mean(cross_val_score(rf, X_train,y_train,scoring='neg_mean_absolute_error', cv=3))

# Tune models GridSearchCV
parameters = {'n_estimators': range(10,300,10), 'criterion': ('mse', 'mae'), 'max_features': ('auto', 'sqrt', 'log2')}

gs = GridSearchCV(rf, parameters,scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)

gs.best_score_
gs.best_estimator_

# Test Ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, tpred_rf)

