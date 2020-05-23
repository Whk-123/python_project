import requests
from bs4 import BeautifulSoup
import traceback


def getHTMLText(url):
    try:
        # 日常模拟浏览器，反反爬
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


def getStockInfo(ilt, html, fpath):
    try:
        if html == "":
            pass
        soup = BeautifulSoup(html, 'html.parser')
        # 发现股票信息存放在tbody标签内
        stockInfo = soup.find('tbody')

        # 一个tr标签对应一只股票
        valueList = stockInfo.find_all("tr")
        # 定义列表keyList，用于匹配股票数据
        keyList = ["序号", "代码", "名称", "现价", "涨跌幅(%)", "涨跌", "涨速(%)", "换手(%)", "量比", "振幅(%)", "成交额", "流通股", "流通市值", "市盈率"]

        # print(type(valueList))

        for i in range(len(valueList)):

            val = str(valueList[i].text).split("\n")
            # 去掉空字符串
            while '' in val:
                val.remove('')
            # print(val)
            for x in range(len(val)):
                key = keyList[x]
                # print(x)
                ilt[key] = val[x]
            # print(ilt)
            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(ilt) + '\n')

    except:
        traceback.print_exc()



# 爬取同花顺股票行情数据
def main():
    # 股票数据保存位置
    output_file = 'D:/TongHuaShunStockInfo.txt'
    # 爬取的页数
    depth = int(input("输入要爬取的股票页数（1页20股，共188页）："))
    infoList = {}
    for i in range(int(depth)):
        i += 1
        # 同花顺股票行情 切换页数时网页url是不发生改变的，根据F12查看网络变化可找出以下 股票url
        url = 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/' + str(i) + '/ajax/1/'

        try:
            html = getHTMLText(url)

            getStockInfo(infoList, html, output_file)

        except:
            print("爬取失败")
    print("爬取完成，股票数据保存在：" + output_file)

if __name__ == '__main__':
    main()
