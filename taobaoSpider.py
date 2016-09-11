# -*- coding:utf-8 -*-
'''
Created on 2016年7月19日
使用多线程下载一个MM的多个相册
分页下载，一次下载一页
'''
__author__ = 'zhm'


import urllib
import urllib2
import re
import os
import requests
import tool
import time
import json
#抓取MM
class Spider:

    #页面初始化
    def __init__(self):
        self.headers={
                'accept-language':'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',
                'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                'origin':'https://mm.taobao.com',
                'referer':'https://mm.taobao.com/search_tstar_model.htm?spm=719.7763510.1998606017.2.vcQ5Zq',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                'x-requested-with':'XMLHttpRequest',
                     }
        self.save = Save();

    #获取MM的信息,得到json格式数据，返回list格式
    def getLists(self,pageIndex):
        siteURL = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
        data={'currentPage':pageIndex,
          'pageSize':str(100),
          }
        r = requests.post(siteURL,headers=self.headers,data=data,timeout=30)
        r.encoding=('GBK')
        if int(r.status_code) != 200:
            print (u"MM列表信息网络访问失败!")
        if int(r.status_code) == 200:
            try:
                #解析json数据
                result = r.json()
            except Exception as e:
                print(u"MM列表信息JSON解析失败！"),e
                result = {}
            if result["status"] == 0:
                print(u"MM列表信息数据查询失败！" )
            elif result["status"] == 1:
                #print(u"MM列表信息数据查询成功！" )
                Lists = result['data']['searchDOList']
                totalPage=result['data']['totalPage']
                totalCount=result['data']['totalCount']
                print (u'总页数:'),totalPage
                print (u'淘宝MM总数：'),totalCount
                return Lists
        else:
            print(u"无法解析服务器的响应内容: \n \t %s " % r.text )
            return

    #传入起止页码，获取MM图片
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
            self.savePageInfo(i)

    #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取淘宝MM列表信息
        lists = self.getLists(pageIndex)
        print u"本次找到美女",len(lists),"位"
        i=0
        for item in lists:
            detailURL = 'https://mm.taobao.com/self/aiShow.htm?userId='+str(lists[i]['userId'])
            self.save.saveDetail(detailURL,item)




class Save:
    def __init__(self):
        self.tool = tool.Tool()
        self.rootpath='D:/taobaoMMT/'
        self.threadpool=[]
        self.threadnum=15  #同时下载的线程数量，不宜设置太多，否则会阻塞
    
    def saveDetail(self,detailURL,item):
        time.sleep(2)   #防止访问太快而导致连接受阻
        #item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
        print u"发现一位模特,名字叫",item['realName']
        print u"身高",item['height'],u"体重",item['weight'],u",她在",item['city']
        print u"正在保存",item['realName'],"的信息"
        #得到个人详情页面代码
        detailPage = self.getDetailPage(detailURL)
#             print 'detailPage+++++++' ,detailPage
        #获取个人简介
        brief = self.getBrief(detailPage)
        #获取所有图片列表
#         images = self.getAllImg(detailPage)
        self.mkdir(item['realName'])
        #保存个人简介
        self.saveBrief(brief,item['realName'],item['userId'])
        #保存头像
        self.saveIcon(item['avatarUrl'],item['realName'],)
        #获取用户相册信息         
        AlbumListAll=self.getAlbumListAll(item['userId'])
        #多线程下载相册列表中的相册
        i=0
        while i<len(AlbumListAll):
            j=0
            while j<self.threadnum and i+j < len(AlbumListAll):
                self.download(item['userId'],item['realName'],AlbumListAll[i+j],i)
                j+=1
            i+=j
            for thread in self.threadpool:
                thread.join(60)  #设置超时参数，60秒之后释放主线程'''
        
    def download(self,userid,usernm,AlbumItem,threadnm):
        crawthread=CrawlerThread(userid,usernm,AlbumItem,threadnm)
        crawthread.start()
        
    #获取MM个人详情页面
    def getDetailPage(self,infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')
    
    #根据userid获取用户所有相册信息
    def getAlbumListAll(self,userid):
        i=1
        AlbumListAll=[]
        while True:
            albumList=self.getAlbumList(userid,i)
            i+=1
            if(albumList != None):
                AlbumListAll.extend(albumList)
            else:
                break
        return AlbumListAll 
       
    #根据userid和page获取相册信息，返回数组[相册id，相册名](照片数量，创建时间暂时不解析)
    def getAlbumList(self,userid,page):
        #此接口获取相册列表
        albumURL='https://mm.taobao.com/self/album/open_album_list.htm'
        data={'_charset':'utf-8',
          'user_id' :str(userid),
          'page':str(page)}
        # 获得json格式的信息 --以下未完成
        r = requests.post(albumURL,data=data,timeout=100)
        r.encoding=('GBK')
        pattern = re.compile('<h4><a href="//.*?album_id=(\d+)&album_flag=0" target="_blank">(.*?)</a></h4>',re.S)
        result = re.findall(pattern,r.text)
        if(result==None or result==[]):
            return None
        else:
            return result
        
    #根据userid,相册id获取用户某一相册内的所有照片地址
    def getPhotoListAll(self,userid,albumID):
        i=1
        PhotoListAll=[]
        while True:
            PhotoList=self.getPhotoList(userid,albumID,i)
            i+=1
            if(PhotoList != None):
                PhotoListAll.extend(PhotoList)
            else:
                break
        return PhotoListAll
            
    #根据userid,相册id及页码获取某一相册内的照片地址列表         
    def getPhotoList(self,userid,albumID,page):
        photoListURL='https://mm.taobao.com/album/json/get_album_photo_list.htm'
        data={'_charset':'utf-8',
          'user_id' :str(userid),
          'album_id':str(albumID),
          'page':str(page)}
        r = requests.post(photoListURL,data=data,timeout=100)
        r.encoding=('GBK')
        PhotoList=[]
        if int(r.status_code) != 200:
            print (u"照片列表信息网络访问失败！"),"userid:",userid
            return None
        if int(r.status_code) == 200:
            try:
                #解析json数据
                result = r.json()
            except Exception as e:
                print(u"照片列表信息JSON解析失败！"),e
                result = {}
                return None
            if result["isError"] == str(1):
                #print(u"照片列表信息数据获取错误！"),
                return None
            elif result["isError"] == str(0):
                #print(u"照片列表信息数据获取成功！"),
                PhotoList = result['picList']
        return PhotoList
    
    
    #获取个人文字简介
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        if(result==None):
            return ""
        else:
            return self.tool.replace(result.group(1))

    '''
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
    def saveImgs(self,images,name,threadnm):
        number = 1
        print threadnm, u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName,threadnm)
            number += 1
    '''

    # 保存头像
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)

    #保存个人简介
    def saveBrief(self,content,name,userid):
        fileName = name + "/" + str(userid) + ".txt"
        f = open(self.rootpath+fileName,"w+")
        print u"正在偷偷保存她的个人信息为",fileName
        f.write(content.encode('utf-8'))


    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
        if(imageURL.find('https',0,len('https')) ==-1):
            imageURL='https:'+imageURL
        urllib.urlretrieve(imageURL,self.rootpath+fileName)
        print u"正在悄悄保存她的一张图片为",fileName
        
    #保存相册中的所有照片    
    def savePhotoAll(self,userid,usernm,albumItem): 
            rstr = r"[\/\\\:\*\?\"\<\>\.\|]"  # '/\:*?"<>.|'
            AlbumName = re.sub(rstr,"",albumItem[1].strip())  #去除首尾空格，剔除非法的文件名字符串
            self.mkdir(usernm+"/"+AlbumName)
            PhotoListAll = self.getPhotoListAll(userid, albumItem[0])#通过相册id获取所有照片地址
            for PhotoList in PhotoListAll:#循环照片地址列表
                index = PhotoList['picUrl'].find('jpg', 0)+3
                picUrlbig = PhotoList['picUrl'][0:index]; #截断jpg后面的文本，保存大图
                self.saveImg(picUrlbig, usernm+"/"+AlbumName+"/"+PhotoList['picId']+".jpg")

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
        
import threading
#多线程由下载MM信息列表改为下载MM照片
class CrawlerThread(threading.Thread):
    '''def __init__(self,url,item,threadnm):
        threading.Thread.__init__(self)
        self.url=url
        self.item=item
        self.threadnm='Thread-'+str(threadnm)
        self.save = Save();'''
    def __init__(self,userid,usernm,AlbumItem,threadnm):
        threading.Thread.__init__(self)
        self.userid=userid
        self.usernm=usernm
        self.albumItem=AlbumItem
        self.threadnm='Thread-'+str(threadnm)
        self.save = Save();
    def run(self):
        try:
#             threadLock.acquire()
            print u'下载线程',self.threadnm,'启动'
            self.save.savePhotoAll(self.userid,self.usernm,self.albumItem)
#             threadLock.release()
        except Exception,e:
            print u'下载失败,MM',self.usernm,'的相册下载失败'
            print u'下载线程',self.threadnm,'退出'
            print e
            return None
# threadLock = threading.Lock()        

#传入页码即可，在此传入了1,表示抓取第1页的MM,一次下载一页
spider = Spider()
# spider.getLists(1)
spider.savePageInfo(1)