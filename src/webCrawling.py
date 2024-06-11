from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from requests.exceptions import RequestException
import time
import random
import os
import shutil
from src import bOCR as bocr

webi_dir = "./src/webimgs/"
driver_dir = os.path.abspath("./src/chromedriver.exe")
titlename=""


def driveropen(url,uid):
    mypath=webi_dir+uid
    if not os.path.isdir(mypath):
        os.mkdir(mypath)
    options = Options()
    options.add_argument('--log-level=3')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    options.add_argument("lang=ko_KR")

    service = Service(executable_path=driver_dir)
    driver = wd.Chrome(service=service, options=options)
    try:
        driver.get(url)
        page = driver.page_source
        image = driver.find_elements(By.CSS_SELECTOR, 'div>img')
        title_element = driver.find_element(By.CSS_SELECTOR,'title')
        titlename = title_element.get_attribute('textContent') if title_element else "No Title"
        imglist = []
        if image:
            imglist = [img.get_attribute("src") for img in image]
            extractImage(imglist, mypath,min(2, len(imglist)))
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
    finally:
        driver.close()
    return page

def extractImage(imglist, mypath,setrange = 0):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    })
    irange = len(imglist) if setrange == 0 else setrange
    for i in range(irange):
        try:
            response = session.get(imglist[i], stream=True)
            if response.status_code == 200:
                with open(os.path.join(mypath, f"{i}.jpg"), 'wb') as out_file:
                    out_file.write(response.content)
            else:
                print(f"HTTP Error {response.status_code} for {imglist[i]}")
        except RequestException as e:
            print(f"Request Error: {e} for {imglist[i]}")
        except Exception as e:
            print(f"Unexpected error: {e} for {imglist[i]}")
        time.sleep(random.uniform(0.8,2))
    session.close()
    imageAnalyze(mypath)
    



def getTitlename():
    return titlename

def imageAnalyze(mypath):
    toTextlist=[]
    items = os.listdir(mypath)
    file_names = [item for item in items if os.path.isfile(os.path.join(mypath, item))]
    sorted_file_names = sorted(file_names, key=lambda x: int(x.split('.')[0]))
    for i in range(len(file_names)):
        toTextlist=bocr.imageToText2(f"{mypath}/{sorted_file_names[i]}")
    # endImageAnalyze(mypath)
    return toTextlist


def endImageAnalyze(mypath):
    for file in os.listdir(mypath):
        file_path = os.path.join(mypath, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("삭제확인")