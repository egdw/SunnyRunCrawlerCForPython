前言:  
     之前一直对于爬虫有一定兴趣,最近刚好为了搞算法.自学了python.经过昨天几个小时的研究.又借用了大家阳光长跑不改密码的优良作风.爬出了大概有1800多条数据.下面将一下具体思路.
    思路:
    网站地址
    http://hzaspt.sunnysport.org.cn/login/
    首先看界面(大体了解如何进行登陆)
    

我们可以发现.就是简单的用户名和密码登录.
看HTML源码:
网站是采用bootstarp(没有软用的信息)

    重点:最简单的form表单.两个参数 username 和 password 请求地址就是当前地址本身.(并没有验证码!!!减轻我识别验证码的压力!!)
     基本了解问题.下面开始解决
实现步骤:
    1.导入python相应的模块
import requests
import pymysql
from bs4 import BeautifulSoup
   大概的流程是读取相应的数据之后,存放到数据库当中
   
   2.伪造请求头
headers = {'content-type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
       
   3.从数据库读取学号.获得集合,进行遍历(不要问我我学号哪里来这么多的)
    

    4.编写相应的模拟登陆函数(login_website),进行模拟登陆
        


    这一块是最重点的地方.首先我发现登陆成功之后,会有一个重定向.我禁止了重定向.发现在登录的时候会产生一个cookieId.如下图.
    

        经过测试.如果不传入这个cookieid就无法实现登陆.
    之后,通过相应的字符串解析.得到了这个id.
    使用get请求加传入cookie数据.即可获取到登陆成功之后的界面(就是下面的地址)   http://hzaspt.sunnysport.org.cn/runner/index.html
    
    5.解析HTML数据
    具体流程就不说了.就是通过解析标签找规律的方式.展示下代码:
    

        
     6.封装数据.
        新建了想应的类和数据库表
        


    最终要时刻到了.就是把获取的数据保存到数据库当中,也就是下面的代码
    

    把相应的数据存入到了数据库当中.

    之后程序继续循环.直到完成所有的学生学号停止(一共获取到了1800多个学生的信息),出于保密.隐藏姓名.
        

    


拿到了这些数据.就可以做很多事,比如分析学生平均速度等等...
    数据不公布呢~

总结:
至此,基本思路都以说明.学习Python一个星期左右.基本的东西编程语言都差不多.Pyhton作为非常高级的语言.我学习的这一段时间有两点明显的感受.
    1.代码短,非常的精练.同样的代码JAVA的代码远远多于Python
    2.第三方库非常厉害!我使用了requests,这比Pyhton自带的库好用多了.
    3.源码已经开源~(https://github.com/egdw/SunnyRunCrawlerCForPython)

    
