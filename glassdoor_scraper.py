# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:54:37 2024

@author: arapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium/tree/master
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    # options = webdriver.ChromeOptions()
    # print("options made, next driver")
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome()
    print("driver made, set window next")
    driver.set_window_size(1120, 1000)
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.occupationParam="' + keyword + '"&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    #Let the page load. Change this number based on your internet speed.
    #Or, wait until the webpage is loaded, instead of hardcoding it.
    time.sleep(slp_time)
    
    #Uncomment for more jobs. This clicks the "Show More" button.
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() 
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() 
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() 
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() 
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() 
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() 
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() 
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click()
    
    #Going through each job in this page ON LEFT COLUMN
    job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv")  #jl for Job Listing. These are the buttons we're going to click.
    

    print("Job Buttons: " + str(len(job_buttons)))   # Works as long as you make sure "Show More" is clicked enough times.  
    
    
    #Getting specific job information or -1 if missing
    for job_button in job_buttons:  
        print("######### Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
        if len(jobs) >= num_jobs:
            break
        
        print("1. next job now")
        job_button.click()  #You might 
        time.sleep(3)
        collected_successfully = False
        print("2. gathering deets")
        
        # GETTING COMPANY NAME, LOCATION, JOB TITLE
        while not collected_successfully:
            try:
                company_name = driver.find_element(By.CSS_SELECTOR, "h4.heading_Heading__BqX5J.heading_Subhead__Ip1aW").text
                location = driver.find_element(By.CLASS_NAME, "JobDetails_location__mSg5h").text                
                try:
                    job_title = driver.find_element(By.CLASS_NAME, "heading_Heading__BqX5J.heading_Level1__soLZs").text
                except NoSuchElementException:
                    job_title = -1

                
                print("Collected success!")
                collected_successfully = True
                
                #debugging company name, job title, and location
                print(company_name)
                print(job_title)
                print(location)
            except: 
                print("Collection Failed")
                time.sleep(3)
        
        # EXPAND JOB DESCRIPTION         ##################################################
        try:
            driver.find_element(By.CLASS_NAME, "JobDetails_showMore___Le6L").click() 
            print("Expanding description...")
            time.sleep(4)
        except:
            time.sleep(4)
            continue
        
        try:
            job_description = driver.find_element(By.CLASS_NAME, "JobDetails_jobDescription__uW_fK.JobDetails_showHidden__C_FOA").text
        except NoSuchElementException:
            job_description = -1
                        
        # GETTING SALARY         ##################################################        
        try:
            salary_estimate = driver.find_element(By.CLASS_NAME, "SalaryEstimate_salaryRange__brHFy").text
        except NoSuchElementException:
            salary_estimate = -1 #You need to set a "not found value. It's important."
        
        # GETTING RATING         ##################################################             
        try:
            rating = driver.find_element(By.CLASS_NAME, 'RatingHeadline_sectionRatingScoreLeft__di1of').text
        except NoSuchElementException:
            rating = -1 #You need to set a "not found value. It's important."
        

        #Printing for debugging
        if verbose:
            print("Job Title: {}".format(job_title))
            print("Salary Estimate: {}".format(salary_estimate))
            print("Job Description: {}".format(job_description))
            print("Rating: {}".format(rating))
            print("Company Name: {}".format(company_name))
            print("Location: {}".format(location))

        #Going to the Company tab...
        
        try:
            company_overviews = driver.find_elements(By.CLASS_NAME, "JobDetails_overviewItemValue__xn8EF")
            # debugging
            # for x in company_overviews:
            #     print(x.text)
            try:
                size = company_overviews[0].text
            except NoSuchElementException:
                size = -1
            
            try:
                founded = company_overviews[1].text
            except NoSuchElementException:
                founded = -1
            
            try:
                type_of_ownership = company_overviews[2].text
            except NoSuchElementException:
                type_of_ownership = -1
            
            try:
                industry = company_overviews[3].text
            except NoSuchElementException:
                industry = -1
            
            try:
                sector = company_overviews[4].text
            except NoSuchElementException:
                sector = -1
            
            try:
                revenue = company_overviews[5].text
            except NoSuchElementException:
                revenue = -1
        except:
            size = -1
            founded = -1
            type_of_ownership = -1           
            industry = -1
            sector = -1
            revenue = -1
            
        # format for company_overviews[] is:
            # size
            # founded
            # type
            # industry
            # sector
            # revenue
            
            
        if verbose:
            print("Size: {}".format(size))
            print("Founded: {}".format(founded))
            print("Type of Ownership: {}".format(type_of_ownership))
            print("Industry: {}".format(industry))
            print("Sector: {}".format(sector))
            print("Revenue: {}".format(revenue))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            
        if company_name in job_description:
            matches = 1
        elif location in job_description:
            matches = 1
        else:
            matches = 0
        
        jobs.append({"Job Title" : job_title,
        "Company" : company_name,
        "Job Description" : job_description,
        "Matches" : matches,
        "Salary Estimate" : salary_estimate,
        "Rating" : rating,
        "Location" : location,
        "Size" : size,
        "Founded" : founded,
        "Type of ownership" : type_of_ownership,
        "Industry" : industry,
        "Sector" : sector,
        "Revenue" : revenue
        })
        #add job to jobs

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.