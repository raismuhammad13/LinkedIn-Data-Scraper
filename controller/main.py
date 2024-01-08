import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.common.exceptions import WebDriverException
import csv
import pandas as pd


import sys
sys.path.insert(0, r'C:\\Users\Aridian Technologies\Desktop\\Office\Desktop\Data Scrappers\\DataScraper_LinkedInData')
from utils.setting import get_settings


def profile_page_data(driver, profile_page_docs):
    # Parsing through each profile page html and extract the profile data
    profile_data = {
    "Name": [],
    "Profile Title": [],
    "Job": [],
    "Company Name": [],
    "Email": [],
    "Location": []
    }
    #Fetching the name of the profile
    name_tag = profile_page_docs.find("h1", class_='text-heading-xlarge inline t-24 v-align-middle break-words')
    profile_data["Name"].append(name_tag.text.strip())
    print(f"Fetchind data form {name_tag.text.strip()}")

    # Fetching the profile tag
    profile_title_tag = profile_page_docs.find("div", class_='text-body-medium break-words')
    profile_data["Profile Title"].append(profile_title_tag.text.strip())
    # print("Profile Title tag line", profile_title_tag.text.strip())

    # Fetching the job title of the profile
    experience_tag = profile_page_docs.find("div",id="experience")
    exp_next_sibling = experience_tag.find_next_sibling("div", class_="SafROhiVFnTqTArSIixYjnkdUqHqwwetStKc")
    exp_next_sibling_cont = exp_next_sibling.find_next_sibling("div", class_="pvs-list__outer-container")
    profile_job_tag = exp_next_sibling_cont.find("div", class_='display-flex flex-wrap align-items-center full-height')
    job = profile_job_tag.find('span', {"aria-hidden":"true"})
    profile_data["Job"].append(job.text.strip())
    # print("Job title", job.text.strip())

    # Fetching the name of a company a profile holder working in
    profile_job_company_tag = exp_next_sibling_cont.find("span", class_='t-14 t-normal')
    company_name_tag = profile_job_company_tag.find('span', {"aria-hidden": "true"})
    company = company_name_tag.text.strip().split("·")[0]
    profile_data["Company Name"].append(company)
    # print("Company Name", company)

    # Fetching the location of profile holder working
    location = profile_page_docs.find('span', class_='text-body-small inline t-black--light break-words')
    profile_data["Location"].append(location.text.strip())
    # print(location.text.strip())

    # Fetching the link for profile info page
    profile_info_page_link = profile_page_docs.find("a", id='top-card-text-details-contact-info')
    profile_contact_info_link = "https://www.linkedin.com" + profile_info_page_link['href']
    driver.find_element(By.ID, "top-card-text-details-contact-info").click()
    time.sleep(2)
    driver.get(profile_contact_info_link)
    time.sleep(1)
    email_page = driver.page_source
    soup = BeautifulSoup(email_page, 'html.parser')
    div_tag = soup.find('a', {"class":"bWCFkfQvJKVrOchJdgENAUvGnHahyLIMLqpA link-without-visited-state t-14", "target":"_blank", "rel":"noopener noreferrer"})
    if div_tag:
        profile_data["Email"].append(div_tag.text.strip())
        # print(div_tag.text.strip())
    else:
        profile_data["Email"].append(None)
        # print(f"email address for {name_tag.text.strip()} does not exists.")
    # print(profile_data)
    # df = pd.DataFrame(profile_data)
    # df.to_csv("Data/profile_data.csv", index=False)
    
    with open("C:\\Users\Aridian Technologies\\Desktop\\Office\Desktop\\Data Scrappers\\DataScraper_LinkedInData\\Data\\linkedInData_New2.csv", mode='a', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        # If the file is empty, write the header
        if csv_file.tell() == 0:
            header = list(profile_data.keys())
            csv_writer.writerow(header)

        # Write data to the CSV file
        for i in range(len(profile_data["Name"])):
            row_data = [profile_data[key][i] for key in profile_data]
            csv_writer.writerow(row_data)

def profile_page_docs(driver, profile_links_list):
    # Parsing main profile page links and return the profile pages html
    profile_page_list = []
    print("we are in profile_page_docs func")
    driver.get(profile_links_list)
    time.sleep(2)
    profile_html_content = driver.page_source
    profile_page_docs = BeautifulSoup(profile_html_content, 'html.parser')
    # profile_page_list.append(profile_page_doc)
    # print(profile_page_list)
    profile_page_data(driver, profile_page_docs)


def profile_page_links(driver, links):
    # Parsing the main page and returing the list of profile links
    print("Getting links from the main page")
    soup = BeautifulSoup(links,'html.parser')
    span_tags = soup.find_all('span', class_= 'entity-result__title-line entity-result__title-line--2-lines')
    link_href_list = []
    for tag in span_tags:
        link_href = tag.find('a').get('href')
        link_href_list.append(link_href_list)
        profile_page_docs(driver, link_href)



def main():
    user = get_settings()["linkedin_logging_credentials"]['user']    
    password = get_settings()["linkedin_logging_credentials"]['password']
    print(user, password)
    # LinkedIn login
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://linkedin.com/uas/login")
    driver.maximize_window()
    time.sleep(.50)
    username = driver.find_element(By.ID, "username")
    username.send_keys(user) #enteremail
    time.sleep(1)
    pword = driver.find_element(By.ID, "password")
    time.sleep(1)
    pword.send_keys(password)       #passw
    time.sleep(1) 
    driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button").click()
    time.sleep(2)

    # Looping through the pages to get the profile links
    for page in range(0,2):
        driver.get(f'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&keywords=azure%20data%20engineer&origin=FACETED_SEARCH&page={page+1}&sid=%3A%40O')
        html_content = driver.page_source
        print(f"Processing for page {page+1}")
        time.sleep(10)

        # Get a list of Links from the main page
        profile_page_links(driver, html_content)
        # Parsing through the main page and return the list of profile pages html as list

if __name__ == "__main__":
    main()