# MTime_imformation
Get the imformation of movie's team as well as its producers and publishers.

## Main code
* `main.py`
* `get_team`<br>
    Get the imformation of team members including director and actors.<br>
* `get_company`<br>
    Get the imformation of producers and publishers.<br>
* `mongo_connect`<br>
    Put the datas into mongodb.<br>
## Operating environment
Based on python3.5 and selenium, first need to install：<br>
1. `selenium`<br>
2. `phantomjs`<br>
3. `mongodb`<br>
4. `pyquery`<br>
## Operation instructions
|star.sh|main.py|get_team.py & get_company.py|mongo_connect|
|:------|:------|:---------------------------|:------------|
|The first file to be executedto call auto_star.py|Initialize datas and then call get_team.py and get_company.py to get the imformation we want.Finally call mongo_connect to store the datas|the main code to crawl content we need|Put the content we have crawled into mongodb|
## Sample
* For the [get_team.py](),let's take [西游降魔篇](http://movie.mtime.com/208325/fullcredits.html) as an example.
* Get it\`s movie name from the folder first, and then enter person\`s page.

### Each item
#### Actor & Director<br>
![](https://github.com/G1704/Selenium-for-URLs/blob/master/github_photo/Item.png "Actor & Director")<br>
<br>
#### Members<br>
![](https://github.com/G1704/Selenium-for-URLs/blob/master/github_photo/Item2.png "Members")<br>
<br>
* For the [get_company.py](), let's take 让子弹飞 for example.
* First get the search page and get the id of this movie. 
![Search](https://github.com/Czt1998/MTime_companies/raw/master/MTime_pic/Search_page)
![id](https://github.com/Czt1998/MTime_companies/raw/master/MTime_pic/id)<br>
Second use the id to enter the page of companies.<br>
![imformation](https://github.com/Czt1998/MTime_companies/raw/master/MTime_pic/Imformation)<br>
* Store the imformation into mongodb. The example is as follow.<br>
* { "_id":  #movie_id, "movie_name":    #movie_id,"year":   #year<br>
            "演员":   #演员列表, "l_company": #发行公司列表, "p_company":   #制作公司列表 }<br>
![imformation](https://github.com/Czt1998/MTime_companies/blob/master/MTime_pic/1211918294.jpg)
