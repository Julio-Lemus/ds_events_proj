# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:02:30 2024

@author: 17jul
"""
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('eda_data.csv')

# choose relevant features
df.columns

df_model = df[['salary_avg', 'Rating', 'Size', 'Type of ownership', 'Industry',
             'Sector', 'Revenue', 'num_comp', 'Employer Provided', 'job_state', 'company_age', 'planning_yn', 'customer_segmentation_yn',
'A/B_yn', 'kpi_metrics_yn', 'customer_behavior_yn', 'forecasting_yn',
'python_yn', 'ga4_yn', 'html_yn', 'sprout_yn', 'sf_yn', 'excel_yn',
'adobe_yn', 'g_ads_yn', 'power_bi_yn', 'powerpoint_yn', 'meta_yn',
'tableau_yn', 'sql_yn', 'seniority', 'desc_len', 'job_simplified']]
#%%
# get dumy data
df_dum = pd.get_dummies(df_model)
#drop -1 salary_avg here
#%%
# train test split
from sklearn.model_selection import train_test_split


X = df_dum.drop('salary_avg', axis =1)
y = df_dum.salary_avg.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#%%
#model prediciton:
#%%
# multiple linear regression - STATS MODEL
import statsmodels.api as sm

X_sm = X = sm.add_constant(X, prepend=False)
model = sm.OLS(y,X_sm.astype(float))
model.fit().summary()

#%%
# multiple linear regression - SKLEARN MODEL
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
import seaborn as sns

lm = LinearRegression()
lm.fit(X_train,y_train)

np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))
# -260980.3073418915 <-- not good
#%%
# lasso regression
lm_l = Lasso(alpha=310)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))
#-14796 with alpha=310... with features not normalized

alpha = []
error = []

for i in range(1,1000):
    alpha.append(i)
    lml = Lasso(alpha=(i))
    error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3)))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]

#%%
# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error', cv= 3))
# -14075.990195989749

#%%
# tune using gridsearch
from sklearn.model_selection import GridSearchCV

# Ken method
parameters = {'n_estimators':range(10,300,10), 'criterion':('squared_error','absolute_error'), 'max_features':('auto','sqrt','log2')}

grid = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
grid.fit(X_train,y_train)
grid.best_params_
#{'criterion': 'absolute_error', 'max_features': 'sqrt', 'n_estimators': 270}
print('----------------------')
grid.best_estimator_
#RandomForestRegressor(criterion='absolute_error', max_features='sqrt',
#                      n_estimators=270)
print('----------------------')
grid.best_score_
#-17081.88746670687

#%%
# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = grid.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
#21050.907450910803
mean_absolute_error(y_test,tpred_lml)
#11635.133970159648
mean_absolute_error(y_test,tpred_rf)
#12631.876499999998

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)
#14799.837856342645

#%%
# import pickle
# pickle = {'model': grid.best_estimator_}
# pickle.dump(pickle, open( 'model_file' + ".p", "wb" ) )

# file_name = "model_file.p"
# with open(file_name, 'rb') as pickled:
#     data = pickle.load(pickled)
#     model = data['model']

# model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0]

# list(X_test.iloc[1,:])


























