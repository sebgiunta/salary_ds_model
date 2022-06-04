# -*- coding: utf-8 -*-
"""
Created on Tue May 17 08:49:36 2022

@author: sebgi
"""

# Original code from https://github.com/arapfaik/scraping-glassdoor-selenium/blob/master/glassdoor%20scraping.ipynb

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(num_jobs, verbose):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor
    '''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path="/Users/sebgi/OneDrive/Python/sebs_projects/salary_ds_model/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    # Set the URL, with the keyword already set.
    url = 'https://www.glassdoor.com.au/Job/australia-data-analyst-jobs-SRCH_IL.0,9_IN16_KO10,22.htm'
    driver.get(url)
    jobs = []
    
    # Handle Sign In Window
    
    driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[1]').click()
    time.sleep(2)
    
    try:
        driver.find_element_by_xpath("//span[@alt='Close']").click() #clicking to the X.
        print(' x out worked')
    except NoSuchElementException:
        print(' x out failed')
        pass

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load.
        time.sleep(3)
        
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            
            job_button.click()
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('//*[@class="css-xuk5ye e1tk4kwz5"]').text #WORKING
                    location = driver.find_element_by_xpath('//*[@class="css-56kyx5 e1tk4kwz1"]').text #WORKING
                    job_title = driver.find_element_by_xpath('//*[@class="css-1j389vi e1tk4kwz2"]').text #WORKING
                    job_description = driver.find_element_by_xpath('//*[@class="jobDescriptionContent desc"]').text #WORKING
                    collected_successfully = True
                except:                 
                    time.sleep(1)

            # TODO FROM HERE      
            try:
                salary_estimate = driver.find_element_by_xpath('//*[@class="css-y2jiyn e2u4hf18"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('//*[@class="css-1m5m32b e1tk4kwz4"]').text
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
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
#                 driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
        
                try:
                    size = driver.find_element_by_xpath("//*[@id='CompanyContainer']//*[text()='Size']//following-sibling::*").text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath("//*[@id='CompanyContainer']//*[text()='Founded']//following-sibling::*").text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath("//*[@id='CompanyContainer']//*[text()='Type']//following-sibling::*").text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath("//*[@id='CompanyContainer']//*[text()='Industry']//following-sibling::*").text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath("//*[@id='CompanyContainer']//*[text()='Sector']//following-sibling::*").text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath("//*[@id='CompanyContainer']//*[text()='Revenue']//following-sibling::*").text
                except NoSuchElementException:
                    revenue = -1


            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

                
            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #add job to jobs
            
        #Clicking on the "next page" button      
        try:
            driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div/div[1]/button[7]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.