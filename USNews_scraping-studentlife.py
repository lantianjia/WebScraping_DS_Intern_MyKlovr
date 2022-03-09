from bs4 import BeautifulSoup
import requests
import xlwt
import csv
import pandas as pd
import re



# Obtaining URLs
## School List

school_list = []

rge = range(0,10)
d = {i:i for i in rge}
df = pd.DataFrame(columns=['url'])
for j in range(1, 184):
    html = requests.get('https://premium.usnews.com/best-colleges/search?_sort=rank&_sortDirection=asc&_page={}'.format(j), headers = {
        "Host": "www.usnews.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }).text
    soup = BeautifulSoup(html, 'lxml')    
    
    for i in d:
        li = soup.find('li', id = 'school-%s'%i)
        
        if not li:
            break
        
        h3 = li.h3
        url = h3.a['href']
        
        school_list.append(url)
        
        
data = {
    "school": school_list
}

url_list = pd.DataFrame(data)
pd.set_option('display.max_rows', 2000)
url_list



# Define Requests

import requests
requests.packages.urllib3.disable_warnings()


class SimpleHttp(object):

    def __init__(self, ua=None):
        self.reqsession = requests.session()

        if not ua:
            self.ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        else:
            self.ua = ua
        
        self.err = None


    def send(self, url, headers=None, data=None, post=False, proxy=None, timeout=30, clear=False, tryCount=1):

        # proxy = "127.0.0.1:8888"

        proxies = None
        if proxy:
            proxies = {
                "http": proxy,
                "https": proxy
            }

        if clear:
            self.reqsession.cookies.clear()

        res = None
        for x in range(0, tryCount):
            try:
                if not data and not post:
                    res = self.reqsession.get(url, headers=headers, proxies=proxies, verify=False, timeout=timeout)
                else:
                    res = self.reqsession.post(url, data=data, headers=headers, proxies=proxies, verify=False, timeout=timeout)
            except Exception as e:
                self.err  = e
                continue
            if res:
                break

        return res



# Data Obtaining
## University Student Life Status

http = SimpleHttp()
live_oncampus = []
school_name = []

for i in school_list:
    url = 'https://www.usnews.com/'+i+'/student-life'
    headers = {
        "Host": "www.usnews.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }

    proxy = "127.0.0.1:8866"
    res = http.send(url=url, headers=headers, data=None, post=False, proxy=proxy, timeout=90, clear=True, tryCount=3)
    if res is None:
        print("error", http.err)
        
    else:
        html = res.text
        soup = BeautifulSoup(html, 'lxml')

        loc_temp = soup.find_all('dd')[1].text
        loc = ' '.join(loc_temp.split())
        
        name = soup.find_all(attrs={'class': 'Heading__HeadingStyled-sc-1w5xk2o-0-h2 bmsqcu Heading-sc-1w5xk2o-1 Wakanda__Title-rzha8s-10 kiCVGj'})[0].text

        live_oncampus.append(loc)
        school_name.append(name)

data = {
    "school_name": school_name,
    "content": live_oncampus
}

live_oncampus = pd.DataFrame(data)
pd.set_option('display.max_rows', 2000)
live_oncampus
