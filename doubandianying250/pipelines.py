# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import *
import re
from scrapy.conf import settings

#
# class Doubandianying250Pipeline(object):
#     def process_item(self, item, spider):
#         item["mv_author"] = item["mv_author"].strip()
#         item["mv_content"] = item["mv_content"][0].strip()+item["mv_content"][1].strip()
#
#
#         print(item)
#         return item
class Doubandianying250Pipeline(object):
    def process_item(self, item, spider):
        # item["mv_author"] = item["mv_author"].strip()
        # item["content"] = item["content"][0].strip()+item["mv_content"][1].strip()
        item["content"] = [re.sub(r"\u3000|\n","",i) for i in item["content"]]
        item["content"] = [i.strip() for i in item["content"] if len(i)>0]
        item["content"] ="".join(item["content"])
        item["mv_author"] =item["mv_author"].strip()
        # t = reduce(lambda x, y: str(x) + str(y), list)

        conn = connect(host = 'localhost',port = 3306,user = 'root',password  = '123',database = 'douban',charset = 'utf8')
        cur1 = conn.cursor()
        sql = """insert into doubandianying (name,rk,con,description,peo,author) values("%s","%s","%s","%s","%s","%s")"""%(item["mv_name"],item["mv_rank"],item["content"],item["mv_desc"],item["peo_rank"],item["mv_author"])
        cur1.execute(sql)
        conn.commit()
        cur1.close()
        conn.close()
        return item

        # item["mv_name"], item['mv_rank'], item["peo_rank"], item["mv_author"], item["mv_desc"], item["content"]




        # host = settings['MYSQL_HOSTS']
        # user = settings['MYSQL_USER']
        # psd = settings['MYSQL_PASSWORD']
        # db = settings['MYSQL_DB']
        # c=settings['CHARSET']
        # port=settings['MYSQL_PORT']
        # db=pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=c,port=port)
        # cur=db.cursor()
        # print("mysql connect success")#测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        #sql="insert into gamerank (rank,g_name,g_type,g_status,g_hot) values(%s,%s,%s,%s,%s)" % (item['rank'],item['game'],item['type'],item['status'],item['hot'])
        # cur.execute("insert into doubanmv(mname,rk,peo,author,descri,content) value('%s','%s','%s','%s','%s','%s')",[ item["mv_name"],item['mv_rank'],item["peo_rank"],item["mv_author"],item["mv_desc"] ,item["content"]])
        # db.commit()
        # print("insert sucessfully")

