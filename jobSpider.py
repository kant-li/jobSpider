#! usr/local/bin/python3.4
# encoding:utf-8

from urllib.request import urlopen
from urllib.parse import quote
from urllib.request import Request
from bs4 import BeautifulSoup       # pip install bs4安装，网页解析包，很常用
import re
import csv
import time
# import geetest        # 破解滑动验证码，暂时不用了

# 用于爬取工商信息的两行参数，暂停使用
# GSXT_HOST_FJ = 'http://fj.gsxt.gov.cn'
# GSXT_INDEX_FJ = GSXT_HOST_FJ + '/notice/'

# 字典，每个岗位对应的搜索网址，去掉page值
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
        time.sleep(0.1)         # 兔子急了也咬人，天天爬人家网站，还是要讲道德的，感谢智联招聘提供的信息
        ###名称
        pattern1 = re.compile(r'k">.+公司')
        companyName = pattern1.search(str(companyDescribe))
        data = [keyWord]
        if companyName is not None:
            companyNameClean = companyName.group()[3:]
            if companyNameClean not in cmpList:
                # print(companyNameClean)
                cmpList.append(companyNameClean)
                data.append(companyNameClean)
                ###针对公司寻找链接
                pattern2 = re.compile(r'http://company\.zhaopin\.com/.+\.htm')
                companyDescribe2 = str(companyDescribe)[:80]
                # print(companyDescribe2)
                companyLink = pattern2.search(companyDescribe2)
                if companyLink is not None:
                    # print(companyLink.group())
                    data.append(companyLink.group())
                    companyInfo(url=companyLink.group(), headers=headers, data=data)
        else:
            continue
    return cmpCount


    ##针对职务寻找链接，暂时没什么用了
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

    # 以下代码用于查询企业工商信息，国家企业信用信息网福建省部分反爬虫太强，封IP很厉害，暂停使用
    # print(data[1])
    # time.sleep(6)
    # basic_info = geetest.query_detail(data[1], GSXT_HOST_FJ, GSXT_INDEX_FJ)
    # if basic_info is not None:
    #     full_data = data + basic_info
    # else:
    #     full_data = data + ['未查询到相关信息']
    # print('-'*20 + 'writer')
    # print(full_data)
    # writer.writerow(full_data)

#主流程
if __name__ == "__main__":
    # 打开文件，写入字段名，目前前面4个有用
    csvfile = open('csv_test.csv', 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(csvfile)
    titles = ["岗位类别","公司名称","链接","地址"\
                ,"统一社会信用代码","企业名称","类型","法定代表人","注册资本","成立日期"\
                ,"经营期限自","经营期限至","登记机关","核准日期","登记状态","住所","经营范围"]
    writer.writerow(titles)
    # 根据不同查询页面爬取数据
    for key in urlDict.keys():
        p = 0
        cmpInPage = 30      # 页面内的公司数，用于判定是否末页
        cmpList = []        # 同一个岗位已收集的公司名称，避免重复收集数据
        while cmpInPage > 20:   #如果页面内公司数少于20，则判定为末页，否则继续下一页
            p += 1
            url1 = urlDict[key] + str(p)
            print(key + '-' * 20 + str(p))
            print(url1)
            cmpInPage = jobFind(key, cmpList, url1, headers)
    csvfile.close()         # 记得关闭文件
