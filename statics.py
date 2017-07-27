# -*- coding:utf-8 -*-
'''
Created on 2016年7月26日
对淘宝MM数据进行分析，用图表展示
'''

from pymongo import MongoClient
from pyecharts import Map
from pyecharts import Geo
from extension import mongo_collection
from extension import mongo_collection2

class Statics:

    def regionDistribute(self):
        data=[]
        value=[]
        attr=[]
        regionData = mongo_collection2.find()
        for item in regionData:
            region = item['region'][5:]
            count = item['totalCount']
            data.append((region,count))
            value.append(count)
            attr.append(region)

        map = Map("淘宝淘女郎全国分布图", width=1200, height=600)
        map.add("", attr, value, maptype='china',visual_range=[0, 5000],is_visualmap=True, visual_text_color='#000')
        map.show_config()
        map.render(r"charts/regionDistribute.html")


    def cityDistribute(self):
        data = []
        value = []
        attr = []
        cityData = mongo_collection.aggregate([{'$group': {'_id': '$city', 'num_tutorial': {'$sum': 1}}}])
        for item in cityData:
            city = item['_id']
            if len(city)>3:
                pass
            else:
                city = item['_id'][:-1]
                count = item['num_tutorial']
                data.append((city, count))
                value.append(count)
                attr.append(city)
        geo = Geo("淘宝淘女郎城市分布图", "data from mm.taobao.com", title_color="#fff", title_pos="center",
                  width=1200, height=600, background_color='#404a59')
        attr, value = geo.cast(data)
        geo.add("", attr, value, visual_range=[0, 1000], visual_text_color="#fff", symbol_size=12, is_visualmap=True)
        geo.show_config()
        geo.render(r"charts/cityDistribute.html")


if __name__ == '__main__':
    statics = Statics()
    statics.regionDistribute()
    # statics.cityDistribute() #待完善