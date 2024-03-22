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
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() #uncomment for scraping 30<n<60 jobs
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() #uncomment for scraping 60<n<90 jobs
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() #uncomment for scraping 90<n<120 jobs
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() #uncomment for scraping 90<n<120 jobs

    #Going through each job in this page ON LEFT COLUMN
    job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv")  #jl for Job Listing. These are the buttons we're going to click.
    company_names = driver.find_elements(By.CLASS_NAME, "EmployerProfile_compactEmployerName__LE242")
    locations = driver.find_elements(By.CLASS_NAME, "JobCard_location__rCz3x")
    job_titles = driver.find_elements(By.CLASS_NAME, "JobCard_jobTitle___7I6y")

    print("Job Buttons: " + str(len(job_buttons)))   #always an extra. as long as you make sure "Show More" is clicked enough times.
    print("Company names: " + str(len(company_names)))
    print("Locations: " + str(len(locations)))
    print("Job Titles: " + str(len(job_titles)))    
    
    for company in company_names:
        print(company.text)
        
    
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
        
        
        while not collected_successfully:
            try:
                company_name = company_names[len(jobs)].text
                location = locations[len(jobs)].text
                #job_title = locations[len(job_titles)].text
                
                try:
                    job_title = driver.find_element(By.CLASS_NAME, "heading_Heading__BqX5J.heading_Level1__soLZs").text
                except NoSuchElementException:
                    job_title = -1

                
                print("Collected success!")
                collected_successfully = True
                print(company_name)
                print(job_title)
                print(location)
            except: 
                print("Collection Failed")
                time.sleep(3)
        
        
        # EXPAND JOB DESCRIPTION         ##################################################
        try:
            driver.find_element(By.CLASS_NAME, "JobDetails_showMore___Le6L").click() 
            time.sleep(4)
        except:
            time.sleep(4)
            continue
        
        try:
            job_description = driver.find_element(By.CLASS_NAME, "JobDetails_jobDescription__uW_fK.JobDetails_showHidden__C_FOA").text
            #job_description = driver.find_element(By.CLASS_NAME, "JobDetails_jobDescription__6VeBn.JobDetails_showHidden__trRXQ").text   
        except NoSuchElementException:
            job_description = -1
            
        # GETTING SALARY         ##################################################        
        try:
            #salary_estimate = driver.find_element(By.XPATH, "//div[@class='SalaryEstimate_averageEstimate__xF_7h']").text
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

        #time.sleep(5)
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
            print("Company overviews absent##############################################################")
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

        jobs.append({"Job Title" : job_title,
        "Company" : company_name,
        "Salary Estimate" : salary_estimate,
        "Job Description" : job_description,
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
