# -*-coding:utf-8-*-
import io
import os
import re
from selenium import webdriver
from time import sleep
from mongo_connect import *



def crawler_team(movie_name,movie_id,i):
    # 爬取信息并写入
    url = 'http://search.mtime.com/search/?q=%s' % movie_name
    print(url)
    browser = webdriver.Chrome()
    browser.get(url)
    sleep(0.5)
    content = browser.execute_script("return document.documentElement.outerHTML")
    urls = re.findall(
        '<a pan="M14_SearchIndex_MoreResult_MovieCover" class="pic __r_c_" target="_blank" href="(.*?)">',
        content)
    final_url = ""
    flag = 1
    for url1 in urls:
        browser.get(url1)
        sleep(1)
        content2 = browser.execute_script("return document.documentElement.outerHTML")
        name = re.findall('<h1 style="font-size:35px;" property="v:itemreviewed">(.*?)</h1>', content2)[0]
        if str(name) == str(movie_name):
            final_url = url1
            flag = 0
            break
    # iid = '_id：' + movie_id + '\n'; year = 'year：' + str(i) + '\n'; movie_names = 'Movie_Name：' + Movie_Name + '\n'
    # f.write(iid.encode());  f.write(year.encode()); f.write(movie_names.encode())
    page = dict()
    if flag == 1:
        browser.close()
        print("(_id + Movie_Name + year) only")
        print()
        # f.close()
        print()
    final_url += 'fullcredits.html'
    print(final_url)
    browser.get(final_url)
    sleep(1)
    content = browser.execute_script("return document.documentElement.outerHTML")
    browser.close()

    # 導演特判
    actor = re.findall('<div class="credits_l">(.*?)</dl>                </div>            </div>',
                       content)
    ele1 = dict()
    try:
        actor = re.findall('<h3><a href="(.*?)" target="_blank">(.*?)</a></h3>', actor[0])
        for a in actor:
            ele1[a[1].replace('.', ' ')] = a[0].replace('.', ' ')
        if ele1 == {}:
            print()
        # f.write(str("演员：").encode())
        # f.write(str(ele1).encode())
        # f.write('\n'.encode())
        page["演员"] = ele1
    except:
        pass

    # 編導特判
    ele2 = dict()
    Director = re.findall(
        '<div class="credits_list">.*?<h4>导演 Director</h4>(.*?)</p>                            </div>                    </div>',
        content)
    try:
        Director = re.findall('<a target="_blank" href="(.*?)">(.*?)</a>', Director[0])
        for a in Director:
            ele2[a[1].replace('.', ' ')] = a[0].replace('.', ' ')
        if ele2 == {}:
            print()
        # f.write(str("导演：").encode())
        # f.write(str(ele2).encode())
        # f.write('\n'.encode())
        page["导演"] = ele2
    except:
        pass

    # 其他人員
    mems = re.findall(
        '<div class="credits_list"><h4>(.*?)</h4> ',
        content)
    for mem in mems[1:]:
        lines = re.findall('<div class="credits_list"><h4>%s</h4>(.*?)</div>' % mem,
                           content)
        ele3 = dict()
        try:
            line = re.findall(' <a target="_blank" href="(.*?)">(.*?)</a>', lines[0])
            if line == "":
                continue
            # f.write((str(mem) + "：").encode())
            for a in line:
                ele3[a[1].replace('.', ' ')] = a[0].replace('.', ' ')
            # f.write(str(ele3).encode())
            # f.write('\n'.encode())
            mem = mem.split(' ')[0]
            page[str(mem)] = ele3
        except:
            pass
    print(page)
    return page
    # f.close()


    print("DONE")
    print()


