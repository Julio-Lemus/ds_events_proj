# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:54:37 2024

@author: 17jul
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

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__JBBUV")  #jl for Job Listing. These are the buttons we're going to click.
        company_names = driver.find_elements(By.CLASS_NAME, "EmployerProfile_employerName__8w0tV")
        ratings = driver.find_elements(By.CLASS_NAME, 'EmployerProfile_ratingContainer__TK35e')


        for job_button in job_buttons:  
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            print("clicking job now")
            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            print("job click worked")
            
            time.sleep(8)
            
            # Test for the "Sign Up" prompt and get rid of it.
            # try:
            #     driver.find_element(By.CLASS_NAME, "ModalOverlay").click()
            # except NoSuchElementException:
            #     pass

            time.sleep(.5)

            # try:
            #     driver.find_element(By.CLASS_NAME, "CloseButton").click()  #clicking to the X.
            # except NoSuchElementException:
            #     pass
            
            
            while not collected_successfully:
                try:
                    #company_name = driver.find_element(By.XPATH, "//a[@class='EmployerProfile_employerName__Xemli']").text
                    company_name = company_names[len(jobs)].text
                    location = driver.find_element(By.CLASS_NAME, "JobDetails_location__MbnUM").text
                    job_title = driver.find_element(By.CLASS_NAME, "JobDetails_jobTitle__Rw_gn").text
                    job_description = driver.find_element(By.XPATH, "//*[@id='app-navigation']/div[3]/div[2]/div[2]/div[1]/section/div[1]/div").text
                    print("Collected success!")
                    collected_successfully = True
                except: 
                    time.sleep(3)
            try:
                salary_estimate = driver.find_element(By.XPATH, "//div[@class='SalaryEstimate_averageEstimate__xF_7h']").text
                # salary_estimate = driver.find_element(By.CLASS_NAME,'JobCard_salaryEstimate___m9kY').text
                print(salary_estimate + "editing?")
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
                
            try:
                rating = ratings[len(jobs)].text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
            

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))


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

        # Clicking on the "next page" button
        try:
            driver.find_element(By.CLASS_NAME, 'button_Button__meEg5 button-base_Button__9SPjH').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.