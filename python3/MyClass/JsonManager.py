# -- coding: utf-8 --
# Author: VicoHu
# Date: 2019.4.2
# ProgramName: jsonManager

import json

class jsonManager:
    """
    读写json文件，并返回一个值
    """
    def __init__(self, path, jsonContent=""):
        self.path = path                # 文件路径
        self.jsonContent = ""           # 要写入的json内容
        self.readerContent = ""         # 从文件读取的json的list
        self.writerContent = ""         # 写入json文件的str 内容
        if jsonContent == "":        # 如果jsonContent为默认值，就直接运行reader
            self.reader()
        else:                        # 否则将jsonContent赋值给self.jsonContent，之后运行writer
            self.jsonContent = jsonContent
            self.writer()

    def writer(self):
        """
        json文件写入器
        :return:无返回值
        """
        with open(self.path, 'w') as file:                      # 打开文件
            json.dump(self.jsonContent, file, indent=4)         # 写入json到指定位置，用4个空格作为一个缩进
            file.close()                                        # 关闭文件
        self.writerContent = json.dumps(self.jsonContent, indent=4)        # 把写入文件中相同的json赋值给self.writeContent，4个空格为一个缩进

    def reader(self):
        """
        json文件读取器
        :return:返回读取json的list值
        """
        with open(self.path, 'r') as file:                      # 打开文件
            jsonList = json.load(file)                          # 读取文件的json到jsonList(类型为list)
            file.close()                                        # 关闭文件
        self.readerContent = jsonList                           # 把从文件中读取的json的list赋值给self.readContent
