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
可以看到，浙江、广东、北京的美女最多，宝岛台湾也有少量美女模特在淘女郎上注册。  
![image](https://github.com/zhmhhu/taobaoSpider/raw/master/png/regionDist.png)  
2. 淘宝淘女郎身高分布图
人数最多的是165cm，看来这是美女的标准身高，其次，还有另外两个小高峰，分别是160cm和168cm。这可能分别代表了萝莉型和御姐型美女的标准身高。另外，小于145cm身高的美女也较多，查看了一下数据，这一部分指的是儿童，统计成年美女身高时可以不考虑这一部分数据。身高为0指的是没有填身高数据的美女，同样可以不参予统计。  
![image](https://github.com/zhmhhu/taobaoSpider/raw/master/png/heightstat.png)  
3. 淘宝淘女郎体重分布图  
人数最多的是45KG,其次是48KG和50KG,34KG及以下的指的是儿童，大于60KG只统计了一个总数，未做单独统计。这一部分美女可能已经不是正常体重了吧。  
![image](https://github.com/zhmhhu/taobaoSpider/raw/master/png/weightstat.png)  
4. 淘宝淘女郎血型分布图
这个比较有意思。是不是说明A型血的人普遍长得更漂亮一些，如果是AB型血，还是做男孩子比较好一点。  
![image](https://github.com/zhmhhu/taobaoSpider/raw/master/png/bloodstat.png)  
5. 淘宝淘女郎星座分布图  
直接统计生日并不是很好处理，于是我把它们转换成了星座，从这个结果可以看出，每个星座并没有绝对的数量差别，人数最多的星座Libra(天秤座)与人数最少的星座Aries(白羊座)也没相差多少，这一结论说明，星座决定论是多么扯淡的事情。O(∩_∩)O哈哈~




# 下一步工作
使用机器学习，构造一个评分器，输入人物的特征值，对该人物的颜值进行打分。