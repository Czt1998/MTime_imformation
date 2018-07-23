# -*-coding:utf-8-*-
"""
"""
from pymongo import MongoClient


def data_save(datas):
    # conn = MongoClient('192.168.235.55', port=27017)
    # db = conn['admin']
    # db.authenticate("admin", "123456")
    # db = conn['team_behind_sc']
    # table = db['Filmmaker_page']
    # table.insert(datas)
    conn = MongoClient()
    db = conn.mydb
    db.col.insert(datas)
