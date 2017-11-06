#! usr/local/bin/python3.4
# encoding:utf-8

from urllib.request import urlopen
from urllib.parse import quote
from urllib.request import Request
from bs4 import BeautifulSoup
import re
import csv

url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2039&jl=%E7%A6%8F%E5%BB%BA&sm=0&p='
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

def jobFind(url, headers):
    # req = Request(url=quote(url, safe='/:?='), headers=headers)
    req = Request(url=url, headers=headers)
    response = urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    result = soup.find_all(class_= 'zwmc')
    for jobDescribe in result:
        pattern = re.compile(r'http://jobs\.zhaopin\.com/.+\.htm')
        jobLink = pattern.search(str(jobDescribe))
        if jobLink is not None:
            print(jobLink.group())
            jobInfo(url=jobLink.group(), headers=headers)

def jobInfo(url, headers):
    req = Request(url=url, headers=headers)
    response = urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    result = soup.find(class_= 'terminal-ul clearfix').strings
    detail = soup.find(class_= 'tab-inner-cont').strings
    data = []
    for i in result:
        text = i.strip().replace('\n', ' ')
        if text != '':
            data.append(text)
    for t in detail:
        text = t.strip().replace('\n', ' ')
        if text != '':
            data.append(text)
    print(data)
    writer.writerow(data)


def jobInfoStrip(jobinfo):
    pass

csvfile = open('csv_test.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(csvfile)
for p in range(1,5):
    url1 = url + str(p)
    print('-' * 20 + str(p))
    print(url1)
    jobFind(url1, headers)
csvfile.close()
