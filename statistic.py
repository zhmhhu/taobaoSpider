# -*- coding:utf-8 -*-
'''
Created on 2016年7月26日
对淘宝MM数据进行分析，用图表展示
'''
from pymongo import MongoClient
from pyecharts import Map,Geo,Bar
from extension import mongo_collection
from extension import mongo_collection2
import re

MONGO_URI = 'mongodb://localhost:27017'

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['taobaoMM']


class Statistic:
    def regionDistribute(self):
        data = {}
        mongo_region_dist = mongo_db['regiondist']
        regionData = mongo_collection2.find()
        for item in regionData:
            region = item['region'][5:]
            count = item['totalCount']
            data['region'] = region
            data['totalCount'] = count
            mongo_region_dist.update({'id': data['region']}, data, upsert=True)

    def cityDistribute(self):
        data = {}
        mongo_city_dist = mongo_db['citydist']
        cityData = mongo_collection.aggregate([{'$group': {'_id': '$city', 'num_tutorial': {'$sum': 1}}}])
        for item in cityData:
            city = item['_id']
            if len(city) > 3:
                pass
            else:
                city = item['_id'][:-1] #获取城市地名的方法待完善
                count = item['num_tutorial']
                data['city'] = city
                data['totalCount'] = count
                mongo_city_dist.update({'id': data['city']}, data, upsert=True)


    def height_statistic(self):
        userData = mongo_collection.find()
        h = {'ht0': 0}
        for i in range(144, 192, 1):
            h['ht' + str(i)] = 0
        for item in userData:
            try:
                height = float(item["height"])
            except ValueError:
                height = 0
                h['ht0'] += 1
            if height <= 144:
                h['ht' + str(144)] += 1
            for i in range(145, 191, 1):
                if i == height:
                    h['ht' + str(i)] += 1
            if height >= 191:
                h['ht' + str(191)] += 1
        mongo_height_stat = mongo_db['heightstat']
        for i in h:
            mongo_height_stat.update({'id': i}, {"height": i.replace("ht", ""), "value": h[i]}, upsert=True)

    def weight_statistic(self):
        userData = mongo_collection.find()
        w = {'wt0': 0}
        for i in range(34, 62, 1):
            w['wt' + str(i)] = 0
        for item in userData:
            try:
                weight = float(item["bodyweight"].replace('KG', ''))
            except ValueError:
                weight = 0
                w['wt0'] += 1
            if weight <= 34:
                w['wt' + str(34)] += 1
            for i in range(35, 60, 1):
                if i == weight:
                    w['wt' + str(i)] += 1
            if weight >= 61:
                w['wt' + str(61)] += 1
        mongo_weight_stat = mongo_db['weightstat']
        for i in w:
            mongo_weight_stat.update({'id': i}, {"weight": i.replace("wt", ""), "value": w[i]}, upsert=True)

    def blood_statistic(self):
        userData = mongo_collection.find()
        bloodAll = ["A", "B", "AB", "O"]
        bloodCot = {"A": 0, "B": 0, "AB": 0, "O": 0, "other": 0}
        for item in userData:
            blood = item["blood"].replace('型', '')
            if blood == "":
                bloodCot["other"] += 1
            else:
                for item in bloodAll:
                    if blood == item:
                        bloodCot[item] += 1
        mongo_blood_stat = mongo_db['bloodstat']
        for i in bloodCot:
            mongo_blood_stat.update({'id': i}, {"blood": i, "value": bloodCot[i]}, upsert=True)

    def birthday_statistic(self):
        import time
        mongo_birthday_stat = mongo_db['birthdaystat']
        userData = mongo_collection.find()
        birthdayCot = {"Aries": 0, "Taurus": 0, "Gemini": 0, "Cancer": 0, "Leo": 0, "Virgo": 0,
                       "Libra": 0, "Scorpio": 0, "Sagittarius": 0, "Capricornus": 0, "Aquarius": 0, "Pisces": 0}
        for item in userData:
            myItem = re.findall("(\d+)月(\d+)日", item['birthday'])
            if myItem != None and len(myItem) >= 1:
                birthday = myItem[0]
                # 按星座统计
                t = (1990, int(birthday[0]), int(birthday[1]), 0, 0, 0, 1, 48, 0)
                secs = time.mktime(t)
                if secs >= time.mktime((1990, 3, 21, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 4, 19, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Aries"] += 1
                elif secs >= time.mktime((1990, 4, 20, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 5, 20, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Taurus"] += 1
                elif secs >= time.mktime((1990, 5, 21, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 6, 21, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Gemini"] += 1
                elif secs >= time.mktime((1990, 6, 22, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 7, 22, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Cancer"] += 1
                elif secs >= time.mktime((1990, 7, 23, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 8, 22, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Leo"] += 1
                elif secs >= time.mktime((1990, 8, 23, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 9, 22, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Virgo"] += 1
                elif secs >= time.mktime((1990, 9, 23, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 10, 23, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Libra"] += 1
                elif secs >= time.mktime((1990, 10, 24, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 11, 22, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Scorpio"] += 1
                elif secs >= time.mktime((1990, 11, 23, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 12, 21, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Sagittarius"] += 1
                elif secs >= time.mktime((1990, 12, 21, 0, 0, 0, 1, 48, 0)) or secs <= time.mktime(
                        (1990, 1, 19, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Capricornus"] += 1
                elif secs >= time.mktime((1990, 1, 20, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 2, 18, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Aquarius"] += 1
                elif secs >= time.mktime((1990, 2, 19, 0, 0, 0, 1, 48, 0)) and secs <= time.mktime(
                        (1990, 3, 20, 0, 0, 0, 1, 48, 0)):
                    birthdayCot["Pisces"] += 1

        for i in birthdayCot:
            mongo_birthday_stat.update({'id': i}, {"blood": i, "value": birthdayCot[i]}, upsert=True)


    def sanwei_statistic(self):
        mongo_sanwei_stat = mongo_db['sanweistat']
        userData = mongo_collection.find()
        for item in userData:
            myItem = re.findall("(\d+)-(\d+)-(\d+)", item['sanwei'])
            if myItem != None and len(myItem) >= 1:
                sanwei = myItem[0]
                chest=sanwei[0]
                waist=sanwei[1]
                buttock=sanwei[2]
                #待完成
            print(myItem)

    def draw_result(self):
        mongo_region_dist = mongo_db['regiondist']
        regiondist = mongo_region_dist.find({}, {"_id": 0})
        attr = []
        value = []
        for item in regiondist:
            value.append(item['totalCount'])
            attr.append(item["region"])
        map = Map("淘宝淘女郎全国分布图", width=1200, height=600)
        map.add("", attr, value, maptype='china', visual_range=[0, 5000], is_visualmap=True,
                         visual_text_color='#000')
        map.render(r"charts/regionDistribute.html")

        #某些城市的地理坐标无法正确获取，故绘图结果不不正确，待完善
        '''mongo_city_dist = mongo_db['citydist']
        citydist = mongo_city_dist.find({}, {"_id": 0})
        attr = []
        value = []
        for item in citydist:
            value.append(item['totalCount'])
            attr.append(item["city"])
        geo = Geo("淘宝淘女郎城市分布图", "data from mm.taobao.com", title_color="#fff", title_pos="center",
                  width=1200, height=600, background_color='#404a59')
        geo.add("", attr, value, visual_range=[0, 1000], visual_text_color="#fff", symbol_size=12, is_visualmap=True)
        geo.render(r"charts/cityDistribute.html")'''

        mongo_height_stat = mongo_db['heightstat']
        heightstat = mongo_height_stat.find({}, {"_id": 0})
        attr = []
        value = []
        for item in heightstat:
            value.append(item['value'])
            attr.append(item["height"])
        bar = Bar("淘宝淘女郎身高分布图", "data from mm.taobao.com")
        bar.add("", attr,value)
        bar.render("charts/heightstat.html")

        mongo_weight_stat = mongo_db['weightstat']
        weightstat = mongo_weight_stat.find({}, {"_id": 0})
        attr = []
        value = []
        for item in weightstat:
            value.append(item['value'])
            attr.append(item["weight"])
        bar = Bar("淘宝淘女郎体重分布图", "data from mm.taobao.com")
        bar.add("", attr, value)
        bar.render("charts/weightstat.html")

        mongo_blood_stat = mongo_db['bloodstat']
        bloodstat = mongo_blood_stat.find({}, {"_id": 0})
        attr = []
        value = []
        for item in bloodstat:
            value.append(item['value'])
            attr.append(item["blood"])
        bar = Bar("淘宝淘女郎血型分布图", "data from mm.taobao.com")
        bar.add("", attr, value)
        bar.render("charts/bloodstat.html")

        mongo_birthday_stat = mongo_db['birthdaystat']
        birthdaystat = mongo_birthday_stat.find({}, {"_id": 0})
        attr = []
        value = []
        for item in birthdaystat:
            value.append(item['value'])
            attr.append(item["blood"])
        bar = Bar("淘宝淘女郎生日星座分布图", "data from mm.taobao.com")
        bar.add("", attr, value)
        bar.render("charts/birthdaystat.html")

if __name__ == '__main__':
    statistic = Statistic()
    statistic.regionDistribute()
    statistic.cityDistribute() #待完善
    statistic.weight_statistic()
    statistic.blood_statistic()
    statistic.birthday_statistic()
    statistic.sanwei_statistic()
    #以下是绘图函数，需待统计函数执行完毕之后再执行
    # statistic.draw_result()