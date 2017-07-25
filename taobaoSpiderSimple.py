# -*- coding:utf-8 -*-
'''
Created on 2017年7月19日
爬取淘宝网上所有淘女郎的信息
'''

__author__ = 'zhm'

import requests
from extension import mongo_collection
from extension import mongo_collection2
import userinfo


class Spider:
    # 页面初始化
    def __init__(self):
        # self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.siteURL = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
        self.headers = {
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://mm.taobao.com',
        'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.7763510.1998606017.2.vcQ5Zq',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        }
        self.region=['city:北京','city:上海', 'city:天津', 'city:重庆',
        'prov:河北','prov:河南','prov:湖北','prov:湖南','prov:福建','prov:江苏','prov:江西','prov:广东','prov:广西',
        'prov:海南','prov:浙江','prov:安徽','prov:吉林','prov:辽宁','prov:山东','prov:山西','prov:陕西','prov:新疆',
        'prov:云南','prov:贵州','prov:四川','prov:甘肃','prov:宁夏','prov:青海','prov:西藏','prov:黑龙江','prov:内蒙古',
        'prov:台湾','prov:香港','prov:澳门']
        self.userinfo = userinfo.UserInfo()

    # 获取淘宝MM的信息,得到json格式数据，返回list格式
    def getLists(self, pageIndex,region):
        data = {'currentPage': pageIndex,
        'pageSize': str(100),
        'searchRegion':region
        }
        # 获得json格式的信息
        r = requests.post(self.siteURL, headers=self.headers, data=data, timeout=60)
        r.encoding = ('GBK')
        # content = r.text.encode(r.encoding).decode('utf-8')
        if int(r.status_code) != 200:
            print (u"getLists:数据获取失败!")
        if int(r.status_code) == 200:
            try:
                # 解析json数据
                result = r.json()
            except Exception as e:
                print(u"getLists:JSON解析失败！"), e
                return
            if result["status"] == 0:
                print(u"getLists:查询失败！")
                return
            elif result["status"] == 1:
                Lists = result['data']['searchDOList']
                return Lists
        else:
            print(u"getLists:无法解析服务器的响应内容: \n \t %s " % r.text)
            return

    # 将淘宝MM的信息保存起来
    def savePageInfo(self, pageIndex,region):
        lists = self.getLists(pageIndex,region)
        if(lists == None):
            print u"本次找到美女", 0, u"位,地区",region,u"页数",pageIndex
        else:
            print u"本次找到美女", len(lists), u"位,地区",region,u"页数",pageIndex
            for item in lists:
                print u"发现一位模特,名字叫", item['realName']
                # print u"身高", item['height'], u"体重", item['weight'], u",她在", item['city'], u",点赞人数", item['totalFavorNum']
                # print u"正在偷偷地保存", item['realName'], "的信息"
                # 获取个人详情
                infos = self.userinfo.moduleInfo(str(item['userId']))
                item['detailURL']= 'https://mm.taobao.com/self/aiShow.htm?userId=' + str(item['userId'])
                dictMerged = dict(item, **infos)
                #将基本信息和个人详情合并，存入数据库
                mongo_collection.update({'id': item['userId']}, dictMerged, upsert=True)

    # 根据所在区域获取淘宝MM的信息，返回页面总数及MM总数
    def searchByRegion(self,region):
        data = {'currentPage': 0,
        'pageSize': str(100),
        'searchRegion': region
        }
        r = requests.post(self.siteURL, headers=self.headers, data=data, timeout=30)
        r.encoding = ('GBK')
        if int(r.status_code) != 200:
            print (u"searchByRegion:数据获取失败!")
        if int(r.status_code) == 200:
            try:
                result = r.json()
            except Exception as e:
                print(u"searchByRegion:JSON解析失败！"), e
                return
            if result["status"] == 0:
                print(u"searchByRegion:查询失败！")
                return 0, 0
            elif result["status"] == 1:
                totalPage = result['data']['totalPage']
                totalCount = result['data']['totalCount']
                print (u'总页数:'), totalPage,(u'淘宝MM总数：'), totalCount
                item={}
                item['region']=region
                item['totalCount']=totalCount
                item['totalPage']=totalPage
                mongo_collection2.update({'id': item['totalCount']}, item, upsert=True)
                return totalPage,totalCount
            else:
                print(u"searchByRegion:无法解析服务器的响应内容: \n \t %s " % r.text)
                return


    # 爬虫开始
    def start(self):
        for item in self.region:
            print u"正在查找位于", item, u"的美眉们..."
            totalpage, totalcount = self.searchByRegion(item)
            for x in range(1,int(totalpage)+1):
                self.savePageInfo(x,item)

if __name__ == '__main__':
    spider = Spider()
    spider.start()
