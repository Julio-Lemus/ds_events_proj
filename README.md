# Marketing Analyst Salary Estimator: Project Overview 
* Created a tool that estimates data science salaries (MAE ~ $ 14K) to help marketing analysts negotiate their income when they get a job.
* Scraped 250 job descriptions from glassdoor using python and selenium
* Engineered features from the text of each job description to quantify the value companies put on python, excel, Google ads, and more. 
* Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model. 
* Built a client facing API using flask 

## Code and Resources Used 
**Python Version:** 3.8.18  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle  
**For Web Framework Requirements:**  ```pip install -r requirements.txt```  
**Scraper Github:** https://github.com/arapfaik/scraping-glassdoor-selenium  
**Scraper Article:** https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905  
**Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## YouTube Project Walk-Through
https://www.youtube.com/playlist?list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t

## Web Scraping
Tweaked the web scraper github repo (above) to scrape 250 job postings from glassdoor.com. With each job, we got the following:
*	Job title
*	Salary Estimate
*	Job Description
*	Rating
*	Company 
*	Location
*	Company Size
*	Company Founded Date
*	Type of Ownership 
*	Industry
*	Sector
*	Revenue

## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

*	Parsed numeric data out of salary 
*	Made columns for employer provided salary 
*	Removed rows without salary 
*	Parsed rating out of company text 
*	Made a new column for company state 
*	Transformed founded date into age of company 
*	Made columns for if different skills were listed in the job description:
    * Python  
    * SQL  
    * Excel  
    * Google Analystics 4  
    * Sprout
    * Power BI
    * More
*	Column for simplified job title and Seniority 
*	Column for description length 

## EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables. 

![alt text](https://github.com/Julio-Lemus/ds_salary_proj/blob/main/mkt_analysis_wordcloud.png "Job Description Word Cloud")
![alt text](https://github.com/Julio-Lemus/ds_salary_proj/blob/main/mkt_analyst_by_state.png "Job Count by State")
![alt text](https://github.com/Julio-Lemus/ds_salary_proj/blob/main/analyst_job_corr.png "Correlations")

## Model Building 

First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.   

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.   

I tried three different models:
*	**Multiple Linear Regression** – Baseline for the model
*	**Lasso Regression** – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
*	**Random Forest** – Again, with the sparsity associated with the data, I thought that this would be a good fit. 

## Model performance
The Random Forest model far outperformed the other approaches on the test and validation sets. 
*	**Random Forest** : MAE ~ $12,631
*	**Linear Regression**: MAE ~ $21,050
*	**Lasso Regression**: MAE ~ ~11,635

## Productionization 
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a job listing and returns an estimated salary. 

## Future Considerations
1. Scrape more data - There were only 265 jobs at the time I scrapped the data with many missing data points. This affected the convergance of the modeling. With 30 parameters, I would like to have at least 350 datapoints with good data.
2. In the tutorial, missing data was left as -1. It would be worth dropping columns, rows, or imputation depending on the total of data missing.
3. Finally, I would like to see an index.html page set-up for a clean interface that users can just paste in data and recieve an estimate. As of now, new data is found in a file and the estimate is returned via command line.
