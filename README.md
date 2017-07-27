# taobaoSpider
- 淘女郎爬虫，爬取淘宝网上淘女郎照片，并存储到本地
- 多线程下载，图片下载速度飞快，小心你的硬盘存不下哦
- 依赖的第三方库包括
 1. requests

# taobaoSpiderSimple

- 另一个爬虫，爬取淘宝网上淘女郎的个人信息，并存储到数据库中  
![image](https://github.com/zhmhhu/taobaoSpider/raw/master/png/regioninfo.png)
![image](https://github.com/zhmhhu/taobaoSpider/raw/master/png/userinfoall.png)
- 依赖的第三方库包括
 1. requests
 2. lxml
 3. pymongo


# 待完成

把爬到的信息进行统计分析，对淘宝MM分布，身高体重等特征值进行分析，得出一些有意思的结论。  
由于pyecharts库对于python2的中文乱码问题处理得不是很好，故此部分功能使用python3完成。以后逐步将所有代码都改成python3
1. 淘宝淘女郎全国分布图  
[淘宝淘女郎全国分布图](https://github.com/zhmhhu/taobaoSpider/raw/master/charts/regionDistribute.html)  

2. 淘宝淘女郎城市分布图  
[淘宝淘女郎城市分布图](https://github.com/zhmhhu/taobaoSpider/raw/master/charts/cityDistribute.html)  


# 下一步工作
使用机器学习，构造一个评分器，输入人物的特征值，对该人物的颜值进行打分。