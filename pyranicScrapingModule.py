import requests
import urllib3

from googlesearch import search
import json
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
# }


def qsearch(query, printThat=False, num_results=10):
    results = []
    for j in search(query, num_results):
        results.append(j)
    results.remove(results[0])
    if printThat:
        itera = 0
        for i in results:
            itera = itera + 1
            print(itera, i)
    else:
        return results


# def relatedSearches(query):
#     params = {
#         'api_key': 'demo',
#         'q': 'ai',
#         'search_type': 'autocomplete'
#     }
#
#     # make the http GET request to Scale SERP
#     api_result = requests.get('https://api.scaleserp.com/search', params)
#
#     # print the JSON response from Scale SERP
#     print(json.dumps(api_result.json()))

def relatedSearches(query, num_results=10):
    query = query.split(' ')
    queryWithPlus = '+'.join(query)
    URL = 'https://www.google.com/search?q='+ queryWithPlus

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
    # print(soup.prettify())
    table = soup.find('div', attrs={'class': 'k8XOCe '})



def getQuestions(query,num_results=10,headless=True,gpu=False)->list:
    options = Options()
    

    if(headless): options.add_argument('--headless')
    if(not gpu): options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=options)
    query = "+".join(query.split(" "))
    driver.get(f"https://google.com/search?q={query}")

    question_answers = []


    i = num_results
    while(i<=10):
        question_elements = driver.find_element_by_xpath(f"/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div[{i}]")
        question_elements.click()
        question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH ,f"/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div[{i}]/div[2]/div/div[1]/div[2]/span"))).text
        question_answers.append(question)
        i+=1

    driver.close()

    return question_answers


def get_keywords(query,headless=True,gpu=False)->list:
    options = Options()
    
    if(headless): options.add_argument('--headless')
    if(not gpu): options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options)
    query = "+".join(query.split(" "))
    driver.get(f"https://google.com/search?q={query}")

    relatedKw = []



    row = 1
    column = 1
    while(column<=2):
        try:
            kword = driver.find_element_by_xpath(f"/html/body/div[7]/div/div[9]/div[1]/div/div[4]/div/div/div/div/div/div/div/div[{column}]/div[{row}]/a/div[2]").text
            relatedKw.append(kword)

        except:
            pass

        if(row==4):
            row = 1
            column+=1
        row+=1
        
        
    
    driver.close()
    return relatedKw
