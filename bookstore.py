"""
Auther:Anna
File Name:bookstore.py
建立時間:2023/1/5,下午 08:03
TODO:
    pip install webdriver-manager
    pip install webdriver-manager packaging
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #這行請手動輸入
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

ops=Options()
#ops.add_argument('--hesdless') #無頭模式，沒有視窗
ops.add_argument('--disable-gpu') #也可以註解，預設啟用GPU
#讓瀏覽器不會自動關閉，待程式完成後，最好註解掉
# ops.add_experimental_option('detach',True)

service=Service(ChromeDriverManager().install())
browser=webdriver.Chrome(service=service, options=ops)
url = "https://www.books.com.tw/?loc=tw_logo_001"
browser.get(url)

target=input("想要搜尋的書本是?")
print('開始搜尋',target)

keyword =WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="key"]')))
# keyword = driver.find_element(by='xpath',value='//*[@id="key"]')
# keyword = driver.find_element_by_xpath('//*[@id="key"]')
keyword.send_keys(target)
keyword.send_keys(Keys.ENTER);

print(browser.title)
print(len(browser.page_source))
soup = BeautifulSoup(browser.page_source,"html.parser")
#bsearch=requests.get(url,headers=headers)
#soup=BeautifulSoup(bsearch.text,'lxml')
div = soup.find('div',"table-searchbox")
items = div.find_all('div','table-td')

booklist=[]
count=1

for page in range(1,3):
    print("抓取: 第" + str(page) + "頁 網路資料中...")
    for i in items:
        bName=i.find('h4').a.get('title')
        type=i.find('div','type clearfix').find('p').text
        price=i.find('ul','price clearfix').find('li').text.strip()

        print('書名:',bName)
        print(type)
        print(price)
        booklist.append({"id": count,
                      "書名": bName,
                      "種類": type,
                      "售價": price})
        print("已經擷取:", count, "筆")
        count = count + 1
    btn_xpath ='/html/body/div[6]/div/div/div/div[6]/ul/li[12]/a'
    button=WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, btn_xpath)))
    # button = browser.find_element(by='xpath',value=btn_xpath)
    # button = driver.find_element_by_xpath(btn_xpath)
    button.click()
    time.sleep(10)
# browser.quit()
today=datetime.now()
with open(str(target)+"_博客來搜尋結果"+today.strftime('%Y%m%d')+".json", "w", encoding="utf-8") as fp:
    json.dump(booklist,fp,indent=2,sort_keys=True,ensure_ascii=False)