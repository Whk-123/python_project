import requests
import re
import json

def getHTMLText(url):
    try:
        # 模拟浏览器，反反爬
        headers = {
            # 可通过在浏览器console中输入navigator.userAgent或window.navigator.userAgent获取
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }

        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding

        return r.text
    except:
        return ""


# tlt = re.findall(r'target="_blank"\stitle=\".*?"', html)
def parsePage(ilt, html):
    try:
        # 正则表达式
        # 价格
        plt = re.findall(r'\"p-price\"\:[\d+\.]*', html)
        # 商品名称-----处理的不好，因为京东商品名称的标签有很多不同的干扰项，个人难以排除干净，所以可能有时会爬出一些干扰标签
        tlt = re.findall(r'<em>(.*?)<font\sclass="skcolor_ljg">', html)

        # print(tlt)
        for i in range(len(plt)):

            price = eval(plt[i].split(':')[1])
            # tlt1 = re.findall("<em>(.*?)<font",tlt[i])
            # print(tlt1)
            title = tlt[i]
            # print(title)
            ilt.append([price, title])
    except:
        print("")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))

    # 保存为json文件
    filename = 'Goods1.json'
    with open(filename, 'w') as file_obj:
        # ensure_ascii=False防止中文乱码
        json.dump(ilt, file_obj,ensure_ascii=False)


def main():
    # 搜索的商品名称
    goods = input("输入要查询的商品名称：")
    # 搜索的页数
    depth = int(input("输入要爬取的商品页数："))
    # 京东搜索
    start_url = 'https://search.jd.com/Search?keyword=' + goods
    infoList = []
    for i in range(depth):

        try:
            # 根据京东商品列表页面的规律设置页面（1，3，5，7……）
            url = start_url + '&enc=utf-8&page=' + str(i * 2 + 1)
            html = getHTMLText(url)
            # 去掉干扰含有价格标签的父标签<strong>
            html = re.sub(">\n<strong(.*?)<i>", ":", html)
            # 去掉干扰标签<span>和<img>,这两个标签经常出现在商品名称里
            html = re.sub("<span\sclass(.*?)</span>", "", html)
            html = re.sub("<img\sclass(.*?)/>", "", html)
            # print(html)
            parsePage(infoList, html)

        except:
            continue
    printGoodsList(infoList)



if __name__ == '__main__':
    main()
# #    # 打印提示信息
#     print('URL is:', stockURL)
#     items = {}  # 建立一个空字典，用于信息存储
#     try:
#         soup = BeautifulSoup(html, 'lxml')
#         for tr in soup.find('tbody').find_all('tr'):
#             td_list = tr.find_all('td')
#             items['代码'] = td_list[1].string
#             items['名称'] = td_list[2].string
#             items['现价'] = td_list[3].string
#             items['涨跌幅'] = td_list[4].string
#             lst.writer.writerow(items)
#             print(items)
#             print("保存成功")
#             # 如果保存成功，则继续使用代理
#             lst.proxy_con = 1
#             # print("解析成功")
#             # yield items          #将结果返回
#     except:
#         print("解析失败")
