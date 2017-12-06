#! usr/local/bin/python3.4
# encoding:utf-8

from urllib.request import urlopen
from urllib.parse import quote
from urllib.request import Request
from bs4 import BeautifulSoup
import re
import csv
import time

# url1 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2040&jl=%E7%A6%8F%E5%B7%9E&p='    ##java
# url2 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2039&jl=%E7%A6%8F%E5%B7%9E&p='    ##Android
# url3 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2041&jl=%E7%A6%8F%E5%B7%9E&p='    ##php
# url4 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=864&jl=%E7%A6%8F%E5%B7%9E&p='    ##web前端
# url5 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2038&jl=%E7%A6%8F%E5%B7%9E&p='    ##IOS
# url6 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2042&jl=%E7%A6%8F%E5%B7%9E&p='    ##C
# url7 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E7%A6%8F%E5%B7%9E&'\
#         + 'kw=.net&isadv=0&isfilter=1&sg=3ed3b548f6cd4b41a75bb6f6cfe995d3&p='    ##.net

urlDict = {'java':'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2040&jl=%E7%A6%8F%E5%B7%9E&p=',\
            'android':'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2039&jl=%E7%A6%8F%E5%B7%9E&p=',\
            'php':'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2041&jl=%E7%A6%8F%E5%B7%9E&p=',\
            'web前端':'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=864&jl=%E7%A6%8F%E5%B7%9E&p=',\
            'ios':'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2038&jl=%E7%A6%8F%E5%B7%9E&p=',\
            'C':'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=2042&jl=%E7%A6%8F%E5%B7%9E&p=',\
            '.net':'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E7%A6%8F%E5%B7%9E&'\
                    + 'kw=.net&isadv=0&isfilter=1&sg=3ed3b548f6cd4b41a75bb6f6cfe995d3&p='}

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

def jobFind(keyWord, cmpList, url, headers):
    ##爬区网页
    # req = Request(url=quote(url, safe='/:?='), headers=headers)
    req = Request(url=url, headers=headers)
    response = urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')

    ##针对公司寻找名称、链接
    result = soup.find_all(class_= 'gsmc')
    cmpCount = len(result)      #用于统计页面中的公司总数，如果低于某个设定数值，则到了末页，本值需要返回
    for companyDescribe in result:
        time.sleep(0.1)
        ###名称
        pattern1 = re.compile(r'k">.+公司')
        companyName = pattern1.search(str(companyDescribe))
        data = [keyWord]
        if companyName is not None:
            companyNameClean = companyName.group()[3:]
            if companyNameClean not in cmpList:
                print(companyNameClean)
                cmpList.append(companyNameClean)
                data.append(companyNameClean)
                ###针对公司寻找链接
                pattern2 = re.compile(r'http://company\.zhaopin\.com/.+\.htm')
                companyDescribe2 = str(companyDescribe)[:80]
                # print(companyDescribe2)
                companyLink = pattern2.search(companyDescribe2)
                if companyLink is not None:
                    print(companyLink.group())
                    data.append(companyLink.group())
                    companyInfo(url=companyLink.group(), headers=headers, data=data)
        else:
            continue
    return cmpCount


    ##针对职务寻找链接
    # result = soup.find_all(class_= 'zwmc')
    # for jobDescribe in result:
    #     pattern = re.compile(r'http://jobs\.zhaopin\.com/.+\.htm')
    #     jobLink = pattern.search(str(jobDescribe))
    #     if jobLink is not None:
    #         print(jobLink.group())
    #         jobInfo(url=jobLink.group(), headers=headers)

def jobInfo(url, headers):
    '''根据岗位链接获取具体信息，并写入表格；'''
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
    # print(data)
    writer.writerow(data)

def companyInfo(url, headers, data):
    '''根据公司链接获取具体信息，并写入表格；'''
    req = Request(url=url, headers=headers)
    response = urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    # print(soup)
    result = soup.find(class_= 'comAddress').strings
    for i in result:
        text = i.strip().replace('\n', ' ')
        if text != '':
            data.append(text)
    writer.writerow(data)

#主流程
csvfile = open('csv_test.csv', 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(csvfile)
titles = ["岗位类别","公司名称","链接","地址"]
writer.writerow(titles)
for key in urlDict.keys():
    p = 0
    cmpInPage = 20      # 页面内的公司数，用于判定是否末页
    cmpList = []        # 同一个岗位已收集的公司名称，避免重复收集数据
    while cmpInPage > 10:   #如果页面内公司数少于10，则判定为末页，否则继续下一页
        p += 1
        url1 = urlDict[key] + str(p)
        print(key + '-' * 20 + str(p))
        print(url1)
        cmpInPage = jobFind(key, cmpList, url1, headers)
csvfile.close()
