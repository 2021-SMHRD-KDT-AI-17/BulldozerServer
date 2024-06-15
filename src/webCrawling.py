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
import urllib.parse
import re
from src import bOCR as bocr
from src import validateWeb as vW
from src import validateLangchain as vL

webi_dir = "./src/webimgs/"
driver_dir = os.path.abspath("./src/chromedriver.exe")
titlename=""


def driveropen(url,uid):
    path1= urllib.parse.quote(url, safe='')
    mypath=os.path.join(webi_dir,uid,path1)
    os.makedirs(mypath, exist_ok=True)
    options = Options()
    options.add_argument('--log-level=3')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    options.add_argument("lang=ko_KR")

    service = Service(executable_path=driver_dir)
    driver = wd.Chrome(service=service, options=options)
    webRes=False
    titlename=""
    try:
        driver.get("http://"+url)
        page = driver.page_source
        image = driver.find_elements(By.CSS_SELECTOR, 'div img')
        title_element = driver.find_element(By.CSS_SELECTOR,'title')
        titlename = title_element.get_attribute('textContent') if title_element else "No Title"
        if titlename=="불법·유해정보사이트에 대한 차단 안내" or titlename=="잠시만 기다리십시오…":
            return {"response": True,"title":"유해사이트"}
        imglist = []
        if image:
            imglist = [img.get_attribute("src") for img in image]
            print(len(imglist))
            extractImage(imglist, mypath)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        webRes=onlyMyAnalyze(mypath)
        print(webRes)
        driver.close()
        return {"response": webRes,"title":titlename}
    

def extractImage(imglist, mypath):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    })
    ilength=len(imglist)
    iv = 1
    while ilength > 10:
        ilength -= 10
        if ilength <10:
            break
        iv += 1
    ei=0
    for i in range(1,len(imglist),iv):
        try:
            response = session.get(imglist[i], stream=True)
            if response.status_code == 200:
                with open(os.path.join(mypath, f"{ei}.jpg"), 'wb') as out_file:
                    out_file.write(response.content)
                    ei+=1
            else:
                print(f"HTTP Error {response.status_code} for {imglist[i]}")
        except RequestException as e:
            print(f"Request Error: {e} for {imglist[i]}")
        except Exception as e:
            print(f"Unexpected error: {e} for {imglist[i]}")
        time.sleep(random.uniform(0.8,1.8))
    session.close()
    

def imageAnalyze(mypath):
    toTextlist=[]
    items = os.listdir(mypath)
    file_names = [item for item in items if os.path.isfile(os.path.join(mypath, item))]
    sorted_file_names = sorted(file_names, key=lambda x: int(x.split('.')[0]))
    goResList=[]
    for i in range(len(file_names)):
        returntexts=bocr.imageToText(f"{mypath}/{sorted_file_names[i]}")
        if len(returntexts)!=0:
            toTextlist.append(returntexts)
            goResList.append(vL.valid(f"{mypath}/{sorted_file_names[i]}"))
    myRes=vW.validate(toTextlist)
    print(goResList)
    goRes=False
    if all(goResList)==True:
        goRes=True
    print(f"내판단{myRes} 구글판단{goRes}")
    time.sleep(10)
    endImageAnalyze(mypath)
    return myRes

def onlyMyAnalyze(mypath):
    myRes=False
    toTextlist=[]
    try:
        items = os.listdir(mypath)
        file_names = [item for item in items if os.path.isfile(os.path.join(mypath, item))]
        sorted_file_names = sorted(file_names, key=lambda x: int(x.split('.')[0]))
        for i in range(len(file_names)):
            toTextlist.append(bocr.imageToText(f"{mypath}/{sorted_file_names[i]}"))
        myRes=vW.validate(toTextlist)
        print(f"내판단{myRes}")
        endImageAnalyze(mypath)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return myRes
def endImageAnalyze(mypath):
    for file in os.listdir(mypath):
        file_path = os.path.join(mypath, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            os.rmdir(file_path)
    print("삭제확인")