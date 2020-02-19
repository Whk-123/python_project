# -*- coding: utf-8 -*-


# 导入第三方模块
import requests
import re

# 下载网页
url = 'http://www.biquge.tv/0_1/'

# 模拟浏览器发送HTTP请求
response = requests.get(url)
# 编码方式
response.encoding = 'gbk'

# 目标小说的网页源码
html = response.text

# 小说的名字
title = re.findall(r'<meta property="og:novel:book_name" content="(.*?)"/>', html, re.S)[0]
print(title)
# #新建文件
fb = open('%s.txt' % title, 'w', encoding='utf-8')

#获取每一章的信息(章节，URL)
div=re.findall(r'<div id="list">.*?</div>',html,re.S)[0]

chapter_info_list=re.findall(r'<a href="(.*?)">(.*?)</a>',div)

#循环每一个章节，分别下载
for chapter_info in chapter_info_list:
    '''
    chapter_title = chapter_info[1]
    chapter_url = chapter_info[0]
    '''
    chapter_url,chapter_title = chapter_info
    chapter_url = "http://www.biquge.tv" + chapter_url

    #下载章节内容
    chapter_response = requests.get(chapter_url)
    chapter_response.encoding='gbk'
    chapter_html = chapter_response.text
    #提取每个章节正文
    chapter_content = re.findall(r'<div id="content">(.*?)</div>',chapter_html,re.S)[0]
    #清洗数据
    chapter_content = chapter_content.replace(' ','')
    chapter_content = chapter_content.replace('<br />','')
    chapter_content = chapter_content.replace('<br/>','')
    chapter_content = chapter_content.replace('m.biquge7.com','\n')
    chapter_content = chapter_content.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\n')
    chapter_content = chapter_content.replace('\n', '')

    #持久化
    fb.write(chapter_title)
    fb.write(chapter_content)
    print(chapter_url)
