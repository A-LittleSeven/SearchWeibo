# 微博搜索爬虫
## 项目简介
本人，想解决论文数据的问题，所以就有了这个项目，因为数据是以社交网络的短评论为主，而且有一定的倾向性，所以就做了一个微博内容的搜索爬虫。

## 项目所需的依赖
（理论上对版本没有必要的要求）  
1.selenium 3.6.0  
2.requests 2.18.4    
3.lxml 4.1.1   
4.pymysql 0.8.0 (或MySQLdb 1.2.5)   
安装方法：  
> pip install *(以上依赖包)

另外爬虫使用了selenium进行模拟登陆（逆向微博有点麻烦）使用的浏览器版本为Chrome 65.0.3325.162（正式版本） （Win10 X64）  
需要安装 [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html?path=2.37/)（版本 2.37）并且设置系统变量（Path）  
(备注，chromedriver只提供x86版本的下载，但是x64同样兼容)
