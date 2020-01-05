# -*- coding: utf-8 -*- 
# @Time : 2019/12/29 3:09 
# @Author : lattesea 
# @File : 计算总和字体反爬篇test3.py
import requests
import re
from fake_useragent import UserAgent
import base64
from fontTools.ttLib import TTFont
from lxml import etree


class SkySpider(object):
    def __init__(self):
        self.url = 'http://glidedsky.com/level/web/crawler-font-puzzle-1?page={}'

    def get_headers(self):
        # ua = UserAgent()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "_ga=GA1.2.1001174242.1571676446; footprints=eyJpdiI6IjM2aG9pWENqd0ZXK3hKemEzcWhJdFE9PSIsInZhbHVlIjoiczAxQTlTKzBcL0dhckJsUXllRWQyK240UWFuWWdMUitOciszNVpCSHMwc2J6ejJEdDdJRm1KeVJGYld6eTgxd1QiLCJtYWMiOiIwNTc3N2FiMTQyMzZkYjg5MTgyOWY0MGUwNTc5MDBkMmQ0ODQ1YmM5ODYyMmViMTMxOWQzMmVmNjlkNTYxZjU4In0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlpcL0NnSTk5UVBJNXY5amdSWDdLa1d3PT0iLCJ2YWx1ZSI6InFSbGpEU0RDU3hyQzNsbFpLQU5oYkFMZGlHV1RXWVNhOTI2ZSsxQ3lqYW1ISUQ2d0VWbnZJSFpRZlwvV0JuTHpZaWdVZU5WV3hjR0ZrN1l4ZXdQQlRSSUkySFJBc3lmWGRGd25QRHQ2WGZnRmIzK3krYnlMXC9MUm1lY29Na1wvdldvU3hNQ0FNeVwvdVhFeUZGSHhKbXZHd2pINFpaMWNFU0N0ajNjSUJHMHJ3TlE9IiwibWFjIjoiMGQ0OWM2ZjdiNTNjYWM2OTg4YjYwMDY5YWFlNDEwYmYzZWE1YjM2NjQwYmUwNjY0MDViNzA5NDQ1ZmM4NDJlYyJ9; _gid=GA1.2.1226032585.1572901871; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1571676446,1571759255,1572901871; XSRF-TOKEN=eyJpdiI6IjVteHBxYTgyVERcL3pseU9FMWhoaDVRPT0iLCJ2YWx1ZSI6Imc1U240b1wvNHRtaHRJUk1hUFEzdTZ1MXN4cUs4eGpTbDJjUXV5Q1RIWUFBdUpPTXd4d0lyZWtDTkxTRXVKcnY4IiwibWFjIjoiNjNkNjUwNzE3ZjRkYWU0MzRiOWEwOWYwNzUxYWY2YjJhZTk3ZTQ2YTI0MjJkODNjOGY4NGE1YzAxMWViMDhmMiJ9; glidedsky_session=eyJpdiI6IkRPOGhIbU5LNEFwQUY0RUJ6YzJQUEE9PSIsInZhbHVlIjoib1FhaFlHSWhUa2E3dkxvcG5SYkZ2THJ1bnBRdDlEeDdHQ1B3dno3RGdubWc1QU1MQ1wvcmVRa0ZWXC9icmIzK0NpIiwibWFjIjoiMjEyOGRlMmM2MDJhMTkwODYxZjdmNDY3MmViNmZiZWIwNmE4YTZmOWMzYmQ1M2UyNmRkMjFlNTYxZjcxYmQ3OSJ9; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1572903027; _gat_gtag_UA_75859356_3=1",
            "Host": "glidedsky.com",
            "Referer": "http://glidedsky.com/level/web/crawler-font-puzzle-1?page=2",
            "Upgrade-Insecure-Requests": "1",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        return headers

    def parse(self, number):
        response = requests.get(url=self.url.format(number), headers=self.get_headers()).text
        font_base64 = re.findall("base64,(.*?)\) format", response)  # 正则匹配网页中base64加密的字体文件
        b = base64.b64decode(font_base64[0])  # 解密base64
        with open('font_online.ttf', 'wb') as f:  # 生成ttf字体文件
            f.write(b)
        online_font = TTFont('font_online.ttf')
        online_font.saveXML('online.xml')  # 生成xml文件
        true_dict = {}  # 正确的映射字典
        index = 0
        base_uni_list = online_font.getGlyphOrder()[1:]
        for i in base_uni_list:
            true_dict[i] = index
            index += 1
        # print(dict)
        # false_dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        #               'seven': 7, 'eight': 8, 'nine': 9, 'zero': 0}
        false_dict = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
                      '8': 'eight',
                      '9': 'nine', '0': 'zero'}
        html = etree.HTML(response)
        false_number = html.xpath("//div[@class='col-md-1']/text()")
        false_number = list(map(lambda item: re.sub('\s+', '', item), false_number))
        false_number = list(filter(None, false_number))
        middle_list1 = []
        middle_list2 = []
        middle_list3 = []
        true_list = []
        for i in false_number:
            for j in i:
                middle = j.replace(j, false_dict[j])
                middle_list1.append(middle)
            middle_list2.append(middle_list1.copy())
            middle_list1.clear()
        for i in middle_list2:
            for j in i:
                middle = j.replace(j, str(true_dict[j]))
                middle_list1.append(middle)
            middle_list3.append(middle_list1.copy())
            middle_list1.clear()
        for i in middle_list3:
            s = "".join(i)
            true_list.append(int(s))
        result = sum(true_list)
        return result

    def run(self):
        result = 0
        for i in range(1, 1001):
            result += self.parse(i)
            print("第%s页计算结束" % i)
        print(result)


if __name__ == '__main__':
    spider = SkySpider()
    spider.run()
