 # codeing utf-8

"""
created on:2018/06/07
author:Czt
target:获取时光网中电影的公司并存入mongoDB
finished on:2018/06/07
"""

import sys
import requests
import time
import re
import json
import urllib
import urllib.request
from pymongo import MongoClient
from selenium import webdriver
from mongo_connect import *
from imp import reload
reload(sys)
driver = webdriver.PhantomJS()


def crawler_company(movie_name,id,year_0):
    # 通过时光网url的特征，利用quoto将电影名拼接得到目标url
    pre_url = 'http://search.mtime.com/search/?q=' + urllib.request.quote(movie_name)
    print(pre_url)
    driver.get(pre_url)
    time.sleep(1)
    # 利用xpath得到带有电影编号的链接
    urls = driver.find_elements_by_xpath("//div[@class='main']/ul/li/h3/a")
    time.sleep(1)
    print(urls)
    print(len(urls))
    ff = 0
    # 如果找不到，则多找几次
    while len(urls) == 0:
        urls = driver.find_elements_by_xpath("//div[@class='main']/ul/li/h3/a")  # 利用xpath得到带有电影编号的链接
        time.sleep(1)
    # ff为计数器，当重复次数超过11次则认为该电影不存在，写入文件手动判断是否为电影名错误
        ff += 1
        if (ff > 11):
            with open("./movie_null.txt", "a+") as w:
                w.writelines(movie_name + ' ' + id)
            break
    all_urls = [i.get_attribute("href") for i in urls]
    time.sleep(1)
    # 判断电影是否存在，若不存在则为名字不正确或者年份不正确
    count = 0
    for urls in all_urls:
        # 获得电影名与年份
        print(urls)
        driver.get(urls)
        name = driver.find_element_by_xpath("//div[@class='clearfix']/h1").text
        year = driver.find_element_by_xpath("//div[@class='clearfix']/p[@class='db_year']/a").text
        time.sleep(0.5)
        print(type(name)),
        print(name)
        print(type(year)),
        print(year)
        time.sleep(1)
        if name == movie_name and year == year_0:
            time.sleep(1)
            count = 1
            data = get_company(urls, movie_name, id, year_0)
            return data
            time.sleep(1)
            break
        else:
            pass
    if count == 0:
        with open('./movie_failed_' + year_0 + '.txt', "a+")as w:
            w.writelines("Fail in name" + movie_name)
            w.write('\n')


def get_company(urls, movie_name,id,year_0):
    """
    获取制作公司与发行公司
    :param urls: 电影公司信息链接
    :param movie_name: 电影名
    :param id: 电影id
    :return: void
    """
    print("Successfully used")
    w = requests.get(urls + "details.html#company")
    w.encoding = 'utf-8'
    html = w.text
    # print(html)
    p_company = 0
    l_company = 0
    res = {}
    try:
        data = re.findall('<div class="fl wp49">.*?</div>', html)[0]
        all = re.findall('<a href="(.*?)".*?>(.*?)</a>', data)
        zc = {}
        for each in all:
            company_name = each[1]
            company_name = company_name.replace('.','')
            zc[company_name] = each[0]
        res['p_company'] = zc
        p_company = 1
    except:
        #将存取失败的文件写入movie_fail文件
        with open('./movie_failed_' + year_0 + '.txt',"a+")as w:
            w.writelines("No p_company" + movie_name + id)
            w.write('\n')

    try:
        data = re.findall('<div class="fl wp49">.*?</div>', html)[1]
        all = re.findall('<a href="(.*?)".*?>(.*?)</a>', data)
        pc = {}
        for each in all:
            company_name = each[1]
            company_name = company_name.replace('.','')
            pc[company_name] = each[0]
        res['l_campany'] = pc
        l_company = 1
    except:
        # 将存取失败的文件写入movie_fail文件
        with open('./movie_failed_' + year_0 + '.txt', "a+")as w:
            w.writelines("No l_company" + movie_name + id)
            w.write('\n')


    print("store" + '\n')
    res = json.dumps(res)
    s = json.loads(res)
    datas = mongoDB_insert(id, movie_name, s, p_company, l_company,year_0)
    return datas


def mongoDB_insert(id,movie_name,s,p_company,l_company,year_0):
    """
    将公司信息存入mongoDB
    :param id: 电影id
    :param movie_name: 电影名
    :param s: 储存着公司信息的字典
    :return: void
    """
    # l_company与p_company用来判断公司是否存在，若不存在则写入null
    if l_company == 1 and p_company == 1:
        data = {
                'p_company': s['p_company'],
                'l_campany': s['l_campany']
               }
    if l_company == 1 and p_company == 0:
        data = {
                'p_company': "null",
                'l_campany': s['l_campany']
                }
    if l_company == 0 and p_company == 1:
        data = {
                'p_company': s['p_company'],
                'l_campany': "null"
                }
    if l_company == 0 and p_company == 0:
        data = {
                'p_company': "null",
                'l_campany': "null"
                }
    print(data)
    return data
    # db.col.remove()
    # for item in db.col.find():
    #     print(item)
    #     print('\n')
