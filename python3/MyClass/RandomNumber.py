# -- coding: utf-8 --
# Author: VicoHu
# Date: 2019.4.3
# ProgramName: RandomNumber


import random
import os
numpyStatus = True
pltStatus = True
try:
    import matplotlib.pyplot as plt         # 尝试引入matplotlib.pyplot
except ModuleNotFoundError:
    pltStatus = False               # 如果引入失败则让pltStatus的值为false
try:
    import numpy                    # 尝试引入numpy
except ModuleNotFoundError:
    numpyStatus = False             # 如果引入失败则让numpyStatus的值为false
from MyClass.JsonManager import jsonManager as JsonM    # 引入Myclass的JsonManager模块


class randomNumber:
    """
    在设定的范围内，随机生成设定个数的随机数，并且可以设置每个数的重复次数
    设有backDoor机制
    """
    def __init__(self, minLim, maxLim, Num, reLimit=0, backDoor=False, backDoorJsonPath=""):
        self.minLim = minLim			# 随机数的起始值（包含）
        self.maxLim = maxLim			# 随机数的最大值（包含）
        self.Num = Num					# 生成随机数的个数
        self.reLimit = reLimit			# 每个数的生成次数上限，默认值为 0，表示不限次数
        self.backDoor = False			# backdoor开关

        self.backDoorList = []			# backDoor列表
        self.randomNumberlist = []		# 生成的随机数的list
        self.reNumberDict = {}			# 随机数的重复次数dict
        self.randomStatus = True       # random()运行标识符
        self.backDoorJsonPath = backDoorJsonPath        # backDoorJson的path

        if (maxLim - minLim + 1) * reLimit < Num:
            self.randomStatus = False       # 改变random()运行运行标识符为False
            print("Init_Error: 初始化错误，请保证 最大可能数字出现总次数 大于 您所需要随机数个数！！！！")
        if backDoor == True:			# 如果backdoor是打开的
            self.backDoor = backDoor		# 则设置类内backDoor开关为打开
            if os.path.exists(backDoorJsonPath):		# 检查是否存在backDoorJsonPath文件
                self.backDoorJsonPath = backDoorJsonPath		# 如果存在则设置类全局backDoorJsonPath
            else:										# 如果不存在，则设置backDoor开关为关闭
                self.backDoor = False
        else:
            pass

    def backDoorJsonReader(self):
        """
        读取backDoorJson的数据，并赋值给self.backDoorList
        :return:无返回值
        """
        if self.backDoor:				# 如果backDoor开关为打开的，则将json文件内容(list)读取到self.backDoorList
            jsonManager = JsonM(self.backDoorJsonPath)
            self.backDoorList = jsonManager.readerContent
        else:
            pass

    def backDoorJsonWriter(self, inBackDoorList):
        """
        写入backDoorJson的数据
        :param inBackDoorList: 需要写入的backDoor数据
        :return:无返回值
        """
        if os.path.exists(self.backDoorJsonPath):            # 如果存在backDoorJsonPath文件
            jsonManager = JsonM(self.backDoorJsonPath)          # 实例化JsonM，初始化里会读取backDoorJsonPath文件的json
            jsonManager.jsonContent = jsonManager.readerContent + inBackDoorList
                    # 将json文件的list和inBackDoorList拼接，并赋值给jsonContent
            jsonManager.jsonContent = list(set(jsonManager.jsonContent))           # 清除列表中的重复元素
            jsonManager.writer()    # 将jsonContent写入文件
        else:
            jsonManager = JsonM(self.backDoorJsonPath, inBackDoorList)

    def randomCount(self):
        """
        生成随机数的次数统计，并写入到reNumberDict.json
        :return:
        """
        if os.path.exists("reNumberDict.json"):            # 如果存在backDoorJsonPath文件
            jsonManager = JsonM("reNumberDict.json")          # 实例化JsonM，初始化里会读取backDoorJsonPath文件的json
            jsonManager.jsonContent = self.reNumberDict
                    # 将json文件的list和inBackDoorList拼接，并赋值给jsonContent
            jsonManager.writer()    # 将jsonContent写入文件
        else:
            jsonManager = JsonM("reNumberDict.json", self.reNumberDict)

    def random(self):
        """
        内置random版（相对性能低一点）用于按条件生成随机数，并把符合条件的随机数赋值给self.randomNumberlist
        :return:无返回值
        """
        self.backDoorJsonReader()
        if self.randomStatus:       # 检测是否达成运行条件
            pass
        else:               # 不达到就强制退出
            return
        count = 1			# 设置计数器，这个是为了计算生成了几个数
        while count <= self.Num:			# 检测是否超过了所需要的最大数 数量的个数
            RandNum = random.randint(self.minLim, self.maxLim)			# 生成一个随机整数（数的极限为minList和maxList）
            if RandNum in self.backDoorList:            # 如果该随机数出现在backDoorList之中，则跳出本次循环
                continue
            else:
                pass
            if RandNum in self.reNumberDict.keys():			# 如果随机数在重复字典的键中存在
                if self.reNumberDict[RandNum] == self.reLimit:       # 如果该键出现次数等于reLimit(重复最大次数)，则放弃该值
                    continue
                else:
                    self.reNumberDict[RandNum] = self.reNumberDict[RandNum] + 1     # 如果以上条件都满足，则给该键的值加1，表示出现次数加1
            else:					# 如果该随机数没有在重复字典的键中出现过，则添加该键，并给其值为1，表示该键出现一次

                self.reNumberDict[RandNum] = 1
            self.randomNumberlist.append(RandNum)  # 将一个随机数加入到randomNumberList
            count = count + 1				# count计数器加1

    def numpyRandom(self):
        """
        高性能版Random，使用了numpy库。
        用于按条件生成随机数，并把符合条件的随机数赋值给self.randomNumberlist
        :return:无返回值
        """
        self.backDoorJsonReader()
        if self.randomStatus:       # 检测是否达成循环运行条件
            if numpyStatus:         # 检测是否成功引入了numpy
                pass
            else:
                print("未成功引用Numpy模块，已使用内置备用随机数生成器")     # 弹出提示
                self.random()           # 运行内置random的随机数生成器
        else:               # 不达到就强制退出
            return
        count = 1			# 设置计数器，这个是为了计算生成了几个数
        while count <= self.Num:			# 检测是否超过了所需要的最大数 数量的个数
            RandNum = numpy.random.randint(self.minLim, self.maxLim + 1, size=1)			# 生成一个随机整数（数的极限为minList和maxList）
            if RandNum in self.backDoorList:            # 如果该随机数出现在backDoorList之中，则跳出本次循环
                continue
            else:
                pass
            if RandNum.tolist()[0] in self.reNumberDict.keys():			# 如果随机数在重复字典的键中存在
                if self.reNumberDict[RandNum.tolist()[0]] == self.reLimit:       # 如果该键出现次数等于reLimit(重复最大次数)，则放弃该值
                    continue
                else:
                    self.reNumberDict[RandNum.tolist()[0]] = self.reNumberDict[RandNum] + 1     # 如果以上条件都满足，则给该键的值加1，表示出现次数加1
            else:					# 如果该随机数没有在重复字典的键中出现过，则添加该键，并给其值为1，表示该键出现一次

                self.reNumberDict[RandNum.tolist()[0]] = 1
            self.randomNumberlist.append(RandNum.tolist()[0])  # 将一个随机数加入到randomNumberList
            count = count + 1				# count计数器加1

    def reNumberDictViewer(self):
        if numpyStatus:         # 检测是否成功引入了numpy
            if pltStatus:           # 检测是否成功引入了matplotlib.pyplot
                pass
            else:
                print("未成功引入matplotlib绘图模块，未完成绘图功能")
                return
        else:
            print("为成功引入Numpy模块，未完成绘图功能")
            return

        plt.rcParams['font.sans-serif'] = ['SimHei']        # 用来正常显示中文
        x = numpy.array(list(self.reNumberDict.keys()))     # 把self.reNumberDict的 键 依次存入有序列表 x 中
        y = numpy.array(list(self.reNumberDict.values()))       # 把self.reNumberDict的 值 依次存入有序列表 y 中
        count = 1           # 定义一个循环控制器
        xy = []             # 定义一个装有 数据柱 标注 的坐标的list
        while (count < len(x)):         # 用循环将x和y的值，一一对应的放入temp，然后装到xy中
            temp = []
            temp.append(x[count - 1])
            temp.append(y[count - 1])
            xy.append(temp)
            count = count + 1           # 计数器自加一
        title = str(self.minLim) + " 号到 " + str(self.maxLim) + " 号的共 " + str(self.Num) + " 次随机抽取情况"
            # 动态赋值title的内容
        plt.figure(title, figsize=(self.maxLim / 2, 4))     # 设置figure的宽度和高度，以及figure的标题
        plt.title(title)  # 设置图表的标题
        plt.bar(x, y, 0.5, alpha=1, color='b')         # 设置柱状图的x，y信息，柱子的宽度，透明度，颜色
        plt.xticks(numpy.arange(self.minLim, self.maxLim + 1, 1))       # 设置x轴显示的信息
        plt.yticks(numpy.arange(1, self.reLimit + 1, 1))                # 设置y轴显示的信息
        for i in xy:
            plt.annotate("%s" % i[1], xy=i, xytext=(i[0] - 0.1, i[1] + 0.025))       # 用循环，依次标记柱状图的柱子的值
        plt.show()

