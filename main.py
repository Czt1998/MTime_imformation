#codeing utf-8
from get_team import *
from get_company import *
from movie_name_id import *

def main():
    # 获取从2010年到2017年的数据
    years = [u'2010',u'2011',u'2012',u'2013',u'2014',u'2015',u'2016',u'2017']
    for year in years:
        year_0 = year
        # id为字典，电影名作为key，电影id作为value
        id = get_id(year_0)
        # 在调用get_id（）时将电影名切片写入文件./Movie_Name/year_0.txt
        with open("./Movie_Name/" + year_0 + ".txt") as f:
            lines = f.readlines()
            for line in lines:
                time.sleep(1)
                movie_name = line.replace('\n', '')  # 因匹配的需要，将电影名的换行符去掉
                # 初始化要获取的数据
                datas = {}
                data = {'_id':id[movie_name],'movie_name':movie_name,'year':year_0}
                # 获得创作团队信息
                team = crawler_team(movie_name,id[movie_name],year_0)
                # 获得制作公司信息
                company = crawler_company(movie_name,id[movie_name],year_0)
                # 更新datas
                datas.update(data)
                datas.update(team)
                datas.update(company)
                print(datas)
                data_save(datas)

if __name__ == '__main__':
    main()