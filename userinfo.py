#-*- coding:utf-8 -*-
from lxml import html
import requests
import sys
import re


class UserInfo:
    def __init__(self):
        pass

    def serachModelInfo(self,userid):
        headers = {
            'accept-language': 'zh-CN,zh;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'authority': 'https://mm.taobao.com',
            'referer': 'https: // mm.taobao.com / self / model_info.htm?spm = 719.7800760.a312r.22.ee2OiD & user_id = 383571291',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        modelinfoURL = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id =' + str(userid)
        # 获得MM详细资料页面
        requests.adapters.DEFAULT_RETRIES = 10
        s = requests.session()
        s.keep_alive = False

        r = requests.get(modelinfoURL, headers=headers, timeout=30)
        r.encoding = 'GBK'
        selector = html.fromstring(r.text)
        urls = []
        for i in selector.xpath('//div[@class="mm-p-info mm-p-base-info"]/ul/li'):
            item = i.xpath("./span/text()|./p/text()")
            urls.append(item)
        return urls

    def getModuleInfo(self,item=None):
        info ={}
        if len(item)>0:
            info['nickname'] = item[0][0] if len(item[0])>0 else ""
            info['birthday'] = item[1][0] if len(item[1]) > 0 else ""
            info['location'] = item[2][0] if len(item[2]) > 0 else ""
            info['occupation'] = item[3][0] if len(item[3]) > 0 else ""
            info['blood'] = item[4][0] if len(item[4]) > 0 else ""
            info['school'] = item[5][0] if len(item[5]) > 0 else ""
            info['style'] = item[6][0] if len(item[6]) > 0 else ""
            info['bodyheight'] = item[7][0] if len(item[7]) > 0 else ""
            info['bodyweight'] = item[8][0] if len(item[8]) > 0 else ""
            info['sanwei'] = item[9][0] if len(item[9]) > 0 else ""
            info['brasize'] = item[10][0] if len(item[10]) > 0 else ""
            info['footsize'] = item[11][0] if len(item[11]) > 0 else ""
        return info

    def moduleInfo(self,userid):
        urls = self.serachModelInfo(userid)
        infos = self.getModuleInfo(urls)
        return infos

if __name__ == '__main__':
    userinfoclass=UserInfo()
    infos = userinfoclass.moduleInfo('176817195')
    print infos
    # for info in infos:
    #     print info