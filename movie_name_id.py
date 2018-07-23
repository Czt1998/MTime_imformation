#codeing utf-8
import sys
from imp import reload
reload(sys)

def get_id(year_0):
    """
    获取电影id并切片出电影名
    :return: id
    """
    id = {}
    with open("./data/" + year_0 + ".txt", "r")as f:
        fp = f.readlines()
        for line in fp:
            movie_n = line.split('')[0]
            movie_id = line.split('')[1]
            movie_id = movie_id.replace('\n', '')
            id[movie_n] = movie_id
            movie_name = line.split("")[0]
            with open("./Movie_Name/" + year_0 + ".txt", "a+")as m:
                m.write(str(movie_name) + '\n')
            print(movie_name)
    return id

