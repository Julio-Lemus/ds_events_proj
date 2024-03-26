# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 10:11:39 2024

@author: 17jul
"""

import glassdoor_scraper as gs
import pandas as pd
path = "C:/Users/17jul/Documents/ds_salary_proj/chromedriver-win64/chromedriver.exe"


df = gs.get_jobs('marketing analyst', 100, False, path, 15)
df.to_csv('glassdoor_mktanalyst_jobs.csv', index=False)
