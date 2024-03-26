# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:37:51 2024

@author: 17jul
"""

import pandas as pd

CURRENT_YEAR = 2024

df = pd.read_csv('glassdoor_mktanalyst_jobs.csv')

#backup checkpoint ######TESTING PURPOSES
df2 = df.copy()

########################## PARSE SALARY 
salary_clean = df['Salary Estimate'].apply(lambda x: x.split("/hr")[0].replace("$", '') if '/hr' in x else x.split("/yr")[0].replace("$", ''))

salary_min_tmp = salary_clean.apply(lambda x: x.split(" ")[0] if '.' in x else x.split(" ")[0].replace("K", "000"))

df2['salary_min'] =  salary_min_tmp.apply(lambda x: float(x)*2080 if '.' in x else float(x))

salary_max_tmp = salary_clean.apply(lambda x: x.split(" ")[-1] if '.' in x else x.split(" ")[-1].replace("K", "000"))

df2['salary_max'] = salary_max_tmp.apply(lambda x: float(x)*2080 if '.' in x else float(x))

df2['salary_avg'] = (df2.salary_max+df2.salary_min)/2




# #if employer provided
df2['Employer Provided'] = df["Salary Estimate"].apply(lambda x: 1 if x !='-1' else 0)

# ########################## STATE FIELD
df2['job_state'] = df2['Location'].apply(lambda x: x.split(', ')[1] if ', ' in x else x)
df2['job_city'] = df2['Location'].apply(lambda x: x.split(', ')[0] if ', ' in x else x)

# #backup checkpoint ######TESTING PURPOSES
# #df = df2.copy()

# ########################## COMPANY AGE
df2['company_age'] = df['Founded'].apply(lambda x: int(x) if x!='--' else -1).apply(lambda x: x if x==-1 else CURRENT_YEAR-x)

# #backup checkpoint ######TESTING PURPOSES
# #df = df2.copy()

# ##################### PARSING JOB DESCRIPTION

# #backup checkpoint ######TESTING PURPOSES
# #df = df2.copy()


df2['planning_yn'] = df['Job Description'].apply(lambda x: 1 if 'planning' in x.lower() else 0)

df2['customer_segmentation_yn'] = df['Job Description'].apply(lambda x: 1 if 'customer segment' in x.lower() else 0)

df2['A/B_yn'] = df['Job Description'].apply(lambda x: 1 if 'a/b testing' in x.lower() else 0)

# metrics, dimensions, KPi
df2['kpi_metrics_yn'] = df['Job Description'].apply(lambda x: 1 if 'kpi' in x.lower() or 'metrics' in x.lower() or 'dimension' in x.lower() else 0)

#semrush 
df2['customer_behavior_yn'] = df['Job Description'].apply(lambda x: 1 if 'behavior' in x.lower() else 0)

#hubspot 
df2['forecasting_yn'] = df['Job Description'].apply(lambda x: 1 if 'forecast' in x.lower() else 0)

# #python
df2['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 
# #google anlaytics
df2['ga4_yn'] = df['Job Description'].apply(lambda x: 1 if 'google analytics'in x.lower() or 'ga4' in x.lower() or 'r-studio' in x.lower() else 0)

df2['html_yn'] = df['Job Description'].apply(lambda x: 1 if 'html' in x.lower() else 0)

df2['sprout_yn'] = df['Job Description'].apply(lambda x: 1 if 'sprout' in x.lower() else 0)

#salesforce
df2['sf_yn'] = df['Job Description'].apply(lambda x: 1 if 'salesforce' in x.lower() else 0)
df2.sf_yn.value_counts()

#excel
df2['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df2.excel_yn.value_counts()

#adobe
df2['adobe_yn'] = df['Job Description'].apply(lambda x: 1 if 'adobe' in x.lower() or 'marketo' in x.lower() else 0)
df2.adobe_yn.value_counts()

#Google Ad
df2['g_ads_yn'] = df['Job Description'].apply(lambda x: 1 if 'google ad' in x.lower() else 0)
df2.g_ads_yn.value_counts()

#Power BI
df2['power_bi_yn'] = df['Job Description'].apply(lambda x: 1 if 'power bi' in x.lower() else 0)
df2.power_bi_yn.value_counts()

#Power point
df2['powerpoint_yn'] = df['Job Description'].apply(lambda x: 1 if 'powerpoint' in x.lower() or 'presentation' in x.lower() else 0)
df2.powerpoint_yn.value_counts()

#meta
df2['meta_yn'] = df['Job Description'].apply(lambda x: 1 if 'meta' in x.lower() or 'facebook' in x.lower() else 0)

#tablou
df2['tableau_yn'] = df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)
df2.tableau_yn.value_counts()

#sql
df2['sql_yn'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
df2.sql_yn.value_counts()

df2.to_csv('salary_data_cleaned.csv', index=False)


pd.read_csv('salary_data_cleaned.csv')