# 微博搜索爬虫
## 项目简介
为了解决数据问题做的一个简单的爬虫项目

## 项目所需的依赖
1.selenium
2.requests
3.lxml
4.pymysql

另外爬虫使用了selenium进行交互，使用的浏览器版本为Chrome 65.0.3325.162（正式版本） （Win10 X64）  
需要安装 [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html?path=2.37/)（版本 2.37）并且设置系统变量（Path）  
(备注，chromedriver只提供x86版本的下载，但是x64同样兼容)

## 重要函数说明
1.模拟登录函数：  
传入参数为username(用户名)， pwd（密码）， retries（登录失败最大重新尝试次数）， time_for_Ele（等待浏览器加载元素的时间）以及
time_for_Fresh（等待浏览器加载页面的时间）

    login_Weibo(username, pwd, retries = 3, time_for_Ele = 1, time_for_Fresh = 3)

2.会话创建函数：
判断当前dir是否存在cookie并且创建一个微博的持久会话

    start_Session(username, password)

3.微博搜索函数：
通过传入的会话对关键字微博进行搜索，传入参数为sess（返回会话），keywords（关键字），sortedby（可选择搜索是按时间还是按热度）

    search_weibo(sess, keywords, sortedby='time')

4.数据获取函数：
    
    parserContent(string):
        ......
        return Id, Weibo, like, repost_Num, repost_Link, comment_Num, comment_Link, timeStamp, Device


对爬取的微博文本进行数据清洗，返回用户ID，微博内容，点赞数， 转发数， 转发链接， 评论数，评论链接，时间戳以及用户使用设备，如果数据有缺失项则缺失项返回为空。
Id, Weibo, like, repost_Num, repost_Link, comment_Num, comment_Link, timeStamp, Device

    parserComment(url):
        ......
    
对楼上函数爬取内容中的评论链接进行二次爬取，将获得内容       [ida,comment,timestamp] 写入csv文件，如果有缺失项，则该行为空。

# 项目其他细节
1. 如果对您有帮助请Star本项目。 
2. 请不要给微博的服务器造成太大的负担，将爬取间隔时间延长！！！！
3. 一次搜索获取的微博数量有限（大概1000条）

# TODO
1. 完成对时间范围的搜索

