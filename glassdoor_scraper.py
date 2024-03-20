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
    
    #Uncomment for more jobs
    # driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() #uncomment for scraping 30<n<60 jobs
    # time.sleep(5)
    # driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() #uncomment for scraping 60<n<90 jobs
    # time.sleep(5)
    # driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/button').click() #uncomment for scraping 90<n<120 jobs

    #Going through each job in this page ON LEFT COLUMN
    job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv")  #jl for Job Listing. These are the buttons we're going to click.
    company_names = driver.find_elements(By.CLASS_NAME, "EmployerProfile_compactEmployerName__LE242")
    locations = driver.find_elements(By.CLASS_NAME, "JobCard_location__rCz3x")

    print(len(job_buttons))    
    print(len(company_names))
    print(len(locations))    
    
    #Getting specific job information or -1 if missing
    for job_button in job_buttons:  
        print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
        if len(jobs) >= num_jobs:
            break

        print("1. next job now")
        job_button.click()  #You might 
        time.sleep(3)
        collected_successfully = False
        print("2. gathering deets")
        
        time.sleep(3)

        
        while not collected_successfully:
            try:
                company_name = company_names[len(jobs)].text
                location = locations[len(jobs)].text
                
                try:
                    job_title = driver.find_element(By.ID, "jd-job-title-1009072166210").text
                except NoSuchElementException:
                    job_title = -1

                
                print("Collected success!")
                collected_successfully = True
            except: 
                print("Collection Failed")
                time.sleep(3)
        
        #Expand job description        
        try:
            driver.find_element(By.CLASS_NAME, "JobDetails_showMore__j5Z_h").click()
            time.sleep(4)
        except:
            time.sleep(4)
            continue
        
        try:
            job_description = driver.find_element(By.XPATH, "//*[@id='app-navigation']/div[3]/div[2]/div[2]/div[1]/section/div[1]/div[1]").text
            #job_description = driver.find_element(By.CLASS_NAME, "JobDetails_jobDescription__6VeBn.JobDetails_showHidden__trRXQ").text   
        except NoSuchElementException:
            job_description = -1
        
        try:
            #salary_estimate = driver.find_element(By.XPATH, "//div[@class='SalaryEstimate_averageEstimate__xF_7h']").text
            salary_estimate = driver.find_element(By.CLASS_NAME, "SalaryEstimate_averageEstimate__xF_7h").text
        except NoSuchElementException:
            print("salary not found")
            salary_estimate = -1 #You need to set a "not found value. It's important."
            
        try:
            rating = driver.find_element(By.CLASS_NAME, 'RatingHeadline_headline__gxpxJ').text
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
            size_element = driver.find_element(By.XPATH, "//span[text()='Size']/following-sibling::div[@class='JobDetails_overviewItemValue__5TqNi']")
            size = size_element.text
        except NoSuchElementException:
            size = -1
        
        try:
            founded_element = driver.find_element(By.XPATH, "//span[text()='Founded']/following-sibling::div[@class='JobDetails_overviewItemValue__5TqNi']")
            founded = founded_element.text
        except NoSuchElementException:
            founded = -1
        
        try:
            type_element = driver.find_element(By.XPATH, "//span[text()='Type']/following-sibling::div[@class='JobDetails_overviewItemValue__5TqNi']")
            type_of_ownership = type_element.text
        except NoSuchElementException:
            type_of_ownership = -1
        
        try:
            industry_element = driver.find_element(By.XPATH, "//span[text()='Industry']/following-sibling::div[@class='JobDetails_overviewItemValue__5TqNi']")
            industry = industry_element.text
        except NoSuchElementException:
            industry = -1
        
        try:
            sector_element = driver.find_element(By.XPATH, "//span[text()='Sector']/following-sibling::div[@class='JobDetails_overviewItemValue__5TqNi']")
            sector = sector_element.text
        except NoSuchElementException:
            sector = -1
        
        try:
            revenue_element = driver.find_element(By.XPATH, "//span[text()='Revenue']/following-sibling::div[@class='JobDetails_overviewItemValue__5TqNi']")
            revenue = revenue_element.text
        except NoSuchElementException:
            revenue = -1

            
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
        "Revenue" : revenue})
        #add job to jobs

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
