# -- coding: utf-8 --
# Arthor:VicoHu
# Data:2019.3.26
# ProgramName:Internet Spider

import re
import requests
import os

class NetSpider:
    """
    using "requests" to get a website's content of code resource
    """
    def __init__(self, url, pattern="", mothod=""):
        self.url = url                  # 需要爬起的网址
        self.pattern = pattern          # 匹配的正则表达式
        self.mothod = mothod.lower()    # 匹配的模式
        self.match_content = ""         # 匹配完后的内容
        self.content = ""               # 需要爬取网站的内容
        self.contentCoding = ""         # 网站默认的编码格式
        self.webObject = ""             # get函数后，网站的对象

    def start(self):
        """
        完整的调用主要的方法们，完成得到源码，匹配信息，并且返回匹配后的信息
        :return: 返回匹配后的信息
        """
        self.getContent()       # 调用getContent函数
        self.switch()           # 调用switch函数进行第二次内容提取
        return self.match_content

    def getContent(self):
        """
        用requests库get原URL的网页源码，并识别网页的原始编码，并重新进行自动编码
        :return: 先更改内部的self.content，然后返回self.content的值
        """
        self.webObject = requests.get(self.url)        # 获得网址被爬取后的对象
        self.contentCoding = self.webObject.encoding    # 获得网站默认编码
        # self.contentCoding = requests.utils.get_encodings_from_content(self.webObject.text)  # 获得网站默认编码
        self.content = self.webObject.content.decode(self.contentCoding)  # 获得解码后的网络源码
        return self.content  # 返回解码后的网络源码

    def switch(self):                   # 匹配方式的选择模块
        """
        通过__init__初始化的self.mothod可以用于判断所需要的正则匹配模式
        :return:无返回值
        """
        if self.mothod == "match":
            self.match_content = re.match(self.pattern, self.content)
        elif self.mothod == "search":
            self.match_content = re.search(self.pattern, self.content)
        elif self.mothod == "findall":
            self.match_content = re.findall(self.pattern, self.content)
        elif self.mothod == "finditer":
            self.match_content = re.finditer(self.pattern, self.content)
        else:
            print("MothodError")            # 如果没有出现想要的匹配方法，则输出 MothodError

    def printer(self):
        """
        打印原网页的代码，并输出基本格式
        :return: 无返回值
        """
        for item in self.content:           # 遍历整个self.content，遇到>符号的时候，进行换行，如果是其他字符，则正常输出不换行
            if item == ">":
                print(">")
            else:
                print(item, end="")















