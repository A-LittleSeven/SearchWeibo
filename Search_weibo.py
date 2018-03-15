#-*- coding:utf-8 -*-
from __future__ import division
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from requests import Session
from lxml import etree
import os
import pickle
import re
import time
import math
import random
import csv
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#----config of weibo account----
username = ''
password = ''
#----end of config----

#----config of mysql----
host = '127.0.0.1'
usname = 'root'
paswd = ''
database = ''
#----end of config----


header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

def mysql_SetUp():
    try:
        db = MySQLdb.connect(host, usname, paswd, database,use_unicode=0, charset='gb2312')
        cur = db.cursor()
        return db, cur
    except Exception as e:
        pass

def login_Weibo(username, pwd, retries = 3, time_for_Ele = 1, time_for_Fresh = 3):

    url = 'http://weibo.cn'
    brow = webdriver.Chrome()

    try:
        brow.get(url)
        time.sleep(3)
        onclick_login = brow.find_element_by_xpath('/html/body/div[2]/div/a[1]')
        onclick_login.click()
        time.sleep(3)
        login_user = brow.find_element_by_xpath('//*[@id="loginName"]')
        login_user.click()
        login_user.send_keys(username)
        login_pwd = brow.find_element_by_xpath('//*[@id="loginPassword"]')
        login_pwd.click()
        login_pwd.send_keys(pwd)
        login_btm = brow.find_element_by_xpath('//*[@id="loginAction"]')
        login_btm.click()
        time.sleep(5)
        time.sleep(5)
        try:
            #获取Cookies
            if not "cookies" in os.listdir('.'):
                with open('cookies', 'wb') as fp:
                    cookies = brow.get_cookies()
                    fp.write(pickle.dumps(cookies))
                    brow.close()

            return True

        except Exception as e:
            return(e)
    except:
        if retries > 0:
            return login_Weibo(retries-1, time_for_Ele+1, time_for_Fresh+2)
        else:
            return False
            raise Exception('Can not login!')

def start_Session(username, password):
    mysession = Session()
    if not 'cookies' in os.listdir('.'):
        login_Weibo(username, password)
    else:
        try:
            with open('cookies', 'rb') as fp:
                cookies = pickle.loads(fp.read())
                for cookie in cookies:
                    mysession.cookies.set(cookie['name'], cookie['value'])
            return mysession
        except Exception as e:
            return e

def search_weibo(sess, keywords, sortedby='time'):

    url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&sort={}&page='.format(keywords, sortedby)

    cmp_div = re.compile('<div class="c" id="M_.*?>(.*?)<div class="s">')
    cmp_page = re.compile('pas')

    for page in range(1, 100):
        if page % 2 == 0:  # 休眠策略，根据时间调整
            time.sleep(random.randint(7, 18))
        if page % 100 == 0:
            time.sleep(20)
 
        new_url = url + str(page)
        with open('url', 'a') as fp:
            fp.write(new_url)
            fp.write('\n')
        try:
            res = sess.get(new_url, headers=header)
            res.encoding = res.apparent_encoding
            content = res.content.encode('gbk', 'ignore')
        except Exception as e:
            print(e)

        div_page = re.findall(cmp_div, content)

        for i in div_page:
            with open('content.csv', 'a') as fp:
                #在这里写入数据
                file = csv.writer(fp)
                file.writerow([
                    parserContent(i)[0],
                    parserContent(i)[1],
                    parserContent(i)[2],
                    parserContent(i)[3],
                    parserContent(i)[4],
                    parserContent(i)[5],
                    parserContent(i)[6],
                    parserContent(i)[7]
                ])

def parserContent(string):
    #原创内容
    regex_ID = re.compile('<a class="nk".*?>(.*?)</a>', re.S)
    regex_Weibo = re.compile('<span class="ctt">(.*?)&nbsp;', re.S)
    regex_time = re.compile('<span class="ct">(.*?)&nbsp;')
    regex_device = re.compile('<span class="ct">.*?&nbsp;(.*?)</span>')
    regex_likes = re.compile('<a href="https://weibo.cn/attitude.*?>(.*?)</a>')
    regex_repost_link = re.compile('(https://weibo.cn/repost.*?)">(.*?)</a>')
    regex_comment_link = re.compile('(https://weibo.cn/comment.*?)" class="cc">(.*?)</a>')
    try:
        Id = re.findall(regex_ID, string)[0].decode('gbk', 'ignore')
        # Id = Id.decode('gbk', 'ignore')
    except:
        Id = None
    try:
        Weibo = re.sub('<a href.*?>|</a>|<b.*?>|&nbsp|\n|\s|<img src.*?>|<span.*?>|</span>|;', '', re.findall(regex_Weibo, string)[0]).decode('gbk', 'ignore')
        # Weibo = Weibo.decode('gbk', 'ignore')
    except:
        Weibo = None
    try:
        like = re.findall(regex_likes, string)[0].decode('gbk', 'ignore')
    except:
        like = None
    try:
        timeStamp = re.findall(regex_time, string)[0].decode('gbk', 'ignore')
    except:
        timeStamp = None
    try:
        Device = re.findall(regex_device, string)[0].decode('gbk', 'ignore')
    except:
        Device = None
    try:
        repost_Link, repost_Num = re.findall(regex_repost_link, string)[0]
        repost_Num = repost_Num.decode('gbk', 'ignore')
    except:
        repost_Link, repost_Num = None, None
    try:
        comment_Link, comment_Num = re.findall(regex_comment_link, string)[0]
        comment_Num = comment_Num.decode('gbk', 'ignore')
    except:
        comment_Link, comment_Num = None, None           
    return Id, Weibo, like, repost_Num, repost_Link, comment_Num, comment_Link, timeStamp, Device


def parserComment(url):

    url = re.sub('&amp;|#cmtfrm', '', url)
    
    regex_pages = re.compile('<input name="mp".*?value="(.*?)".*?>')
    regex_div = re.compile('<div class="c" id="C_.*?>(.*?)</div>')
    regex_id = re.compile('<a href.*?>(.*?)</a>')
    regex_comment = re.compile('<span class="ctt">(.*?)</span>')
    regex_timestamp = re.compile('<span class="ct">&nbsp;(.*?)&nbsp;')

    res = sess.get(url, headers=header)
    res.encoding = res.apparent_encoding
    try:
        pages = re.findall(regex_pages, res.content)[0]
    except:
        pages = 10

    for page in range(1, int(pages) + 1):
        if page % 3 == 0:  # 休眠策略，根据时间调整
            time.sleep(random.randint(10, 18))
        if page % 100 == 0:
            time.sleep(random.randint(20, 60))
        if page % 502 == 0:
            time.sleep(random.randint(300, 500))

        new_url = url + u'&page={}'.format(page)
        try:
            res = sess.get(new_url, headers=header)
            res.encoding = res.apparent_encoding
            content = res.content.encode('gbk', 'ignore')
        except Exception as e:
            print(e)

        div_page = re.findall(regex_div, content)
        
        for i in div_page:
            try:
                ida = re.findall(regex_id, i)[0].decode('gbk', 'ignore')
            except:
                ida = None
            try:
                comment = re.sub('<a href.*?>|</a>|<b.*?>|&nbsp|\n|\s|<img src.*?>|<span.*?>|</span>|"|;', '', re.findall(regex_comment, i)[0]).decode('gbk', 'ignore')
            except:
                comment = None
            try:
                timestamp = re.findall(regex_timestamp, i)[0]
            except:
                timestamp = None

            with open('short_text.csv', 'a') as fp:
                wt = csv.writer(fp)
                wt.writerow(
                    [ida,
                    comment,
                    timestamp]
                )

if __name__ == '__main__':
    pass

