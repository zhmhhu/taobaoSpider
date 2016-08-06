# -*- coding:utf-8 -*-
'''
Created on 2016年7月19日
多线程爬虫
'''
__author__ = 'zhm'


import urllib
import urllib2
import re
import os
import requests
import tool

#抓取MM
class Spider:

    #页面初始化
    def __init__(self):
#         self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.siteURL = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
        self.headers={
                'accept-language':'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',
                'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                'origin':'https://mm.taobao.com',
                'referer':'https://mm.taobao.com/search_tstar_model.htm?spm=719.7763510.1998606017.2.vcQ5Zq',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                'x-requested-with':'XMLHttpRequest',
                     }

    #获取MM的信息,得到json格式数据，返回list格式
    def getLists(self,pageIndex):
        data={'currentPage':pageIndex,
          'pageSize':str(100),
          }
        # 获得json格式的信息 --以下未完成
        r = requests.post(self.siteURL,headers=self.headers,data=data,timeout=30)
        r.encoding=('GBK')
#         content = r.text.encode(r.encoding).decode('utf-8')
        if int(r.status_code) != 200:
            print (u"数据获取失败!")
        if int(r.status_code) == 200:
            try:
                #解析json数据
                result = r.json()
            except Exception as e:
                print(u"JSON解析失败！"),e
                result = {}
            if result["status"] == 0:
                print(u"查询失败！" )
            elif result["status"] == 1:
                print(u"查询成功！" )
                Lists = result['data']['searchDOList']
                totalPage=result['data']['totalPage']
                totalCount=result['data']['totalCount']
                print (u'总页数:'),totalPage
                print (u'淘宝MM总数：'),totalCount
                return Lists
        else:
            print(u"无法解析服务器的响应内容: \n \t %s " % r.text )
            return

   

    #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取淘宝MM列表信息
        lists = self.getLists(pageIndex)
        print u"本次找到美女",len(lists),"位"
        i=1
        for item in lists:

            #item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
            print u"发现一位模特,名字叫",item['realName']
            print u"身高",item['height'],u"体重",item['weight'],u",她在",item['city']
            print u"正在偷偷地保存",item['realName'],"的信息"
#             print u"又意外地发现她的个人地址是",item['avatarUrl']
            #个人详情页面的URL
            detailURL = 'https://mm.taobao.com/self/aiShow.htm?userId='+str(item['userId'])
            self.download(detailURL,item,'Thread-'+str(i))
            i+=1
    def download(self,url,item,tName):
        crawthread=CrawlerThread(url,item,tName)
        crawthread.start()            
        
    #传入起止页码，获取MM图片
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
            self.savePageInfo(i)
import threading
import time            
class CrawlerThread(threading.Thread):
    def __init__(self,url,item,tName):
        threading.Thread.__init__(self)
        self.url=url
        self.item=item
        self.tName=tName
        self.tool = tool.Tool()
        self.rootpath='D:/taobaoMM/'
    def run(self):
        try:
            self.saveDetail(self.url,self.item,self.tName)
        except Exception,e:
            print u'下载失败',self.url
            print u'线程',self.tName,'退出'
            print e
            return None
    def saveDetail(self,detailURL,item,tName):
    #得到个人详情页面代码
        detailPage = self.getDetailPage(detailURL)
#             print 'detailPage+++++++' ,detailPage
        #获取个人简介
        brief = self.getBrief(detailPage)
        #获取所有图片列表
        images = self.getAllImg(detailPage)
        self.mkdir(item['realName'])
        #保存个人简介
        self.saveBrief(brief,item['realName'],tName)
        #保存头像
        self.saveIcon(item['avatarUrl'],item['realName'],tName)
        #保存图片
        self.saveImgs(images,item['realName'],tName)
        
    #获取MM个人详情页面
    def getDetailPage(self,infoURL):
        time.sleep(2)   #防止访问太快而导致连接受阻
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')

    #获取个人文字简介
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        if(result==None):
            return ""
        else:
            return self.tool.replace(result.group(1))

    #获取页面所有图片
    def getAllImg(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        #个人信息页面所有代码
        content = re.search(pattern,page)
        if(content==None):
            return
        else: 
            #从代码中提取图片
            patternImg = re.compile('<img.*?src="(.*?)"',re.S)
            images = re.findall(patternImg,content.group(1))
            return images


    #保存多张写真图片
    def saveImgs(self,images,name,tName):
        number = 1
        print tName, u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName,tName)
            number += 1

    # 保存头像
    def saveIcon(self,iconURL,name,tName):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName,tName)

    #保存个人简介
    def saveBrief(self,content,name,tName):
        fileName = name + "/" + name + ".txt"
        f = open(self.rootpath+fileName,"w+")
        print tName,u"正在偷偷保存她的个人信息为",fileName
        f.write(content.encode('utf-8'))


    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName,tName):
        if(imageURL.find('https',0,len('https')) ==-1):
            imageURL='https:'+imageURL
            
        urllib.urlretrieve(imageURL,self.rootpath+fileName)
        
        ''''u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(self.rootpath+fileName, 'wb')
        f.write(data)'''
        print tName,u"正在悄悄保存她的一张图片为",fileName
#         f.close()

    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        truePath=self.rootpath+path
        isExists=os.path.exists(truePath)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"偷偷新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(truePath)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False

#传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
spider = Spider()
# spider.getLists(1)
spider.savePagesInfo(1,2)