# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

from pylab import *
import re
from random import *

class Data:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.dis = []
		self.cluster = 0

traindata = []

# 读取测试数据集，存储
def readdata():
	fp = open('g2-2-30.txt', 'r')
	trainlist = []
	for line in fp.readlines():
		line = line.strip()
		X = re.split(r'\s+', line)
		newdata = Data(int(X[0]), int(X[1]))
		trainlist.append(newdata)
	fp.close()
	return trainlist

# 某点与簇质心的欧式距离
def cal_dis(x, y, x_center, y_center):
	temp1 = pow((x - x_center), 2)
	temp2 = pow((y - y_center), 2)
	res = temp1 + temp2
	res1 = sqrt(res)
	return sqrt(res1)


def kmeans_cluster(center):
	# 依次循环每一个质心，计算每个点与每个质心的距离
	global traindata

	# 对每个点的距离列表清空
	for point in traindata:
		point.dis = []
		point.cluster = 0

	for center1 in center:
		x_center = float(center1[0])
		y_center = float(center1[1])
		for point in traindata:
			x = point.x
			y = point.y
			dis = cal_dis(x, y, x_center, y_center)
			point.dis.append(dis)

	# 将每个点划分到某个簇内
	for point in traindata:
		min_dis = min(point.dis)
		cho_cluster = point.dis.index(min_dis)
		point.cluster = cho_cluster+1

	# 重新计算质心
	new_center = []
	for i in range(len(center)):
		new_cluster = Data(0, 0)
		cluster_num = 0
		for point in traindata:
			if point.cluster == i+1:
				new_cluster.x += point.x
				new_cluster.y += point.y
				cluster_num += 1
		new_center.append((float(new_cluster.x/cluster_num), float(new_cluster.y/cluster_num)))
	return new_center


# kmeans 主程序
def kmeans_main(k_num):
	global traindata
	train_num = len(traindata)
	center = []  # 初始质心
	k = k_num
	# 随机初始化K个质心
	while k:
		cen = randint(1, train_num)
		center.append((traindata[cen].x, traindata[cen].y))  # 添加质心
		k -= 1

	# 迭代调用函数计算簇质心
	iter_num = 1000
	while iter_num:
		new_center = kmeans_cluster(center)
		#print center[:], new_center[:]
		if new_center[0][0] == center[0][0]:
			break
		center = new_center
		iter_num -= 1
	print "最终质心位置：", center[:]

	# 绘制簇质心和簇中各点的散点图
	global traindata
	# 绘制初始散点图
	printlist = []
	leibie = range(1, k_num+1)
	for t in leibie:
		printlist.append([])
	for i in range(len(traindata)):
		for j in leibie:
			if traindata[i].cluster == j:
				printlist[j-1].append(i)
	print "每个簇点的个数是",
	for p in range(len(printlist)):
		print len(printlist[p]),
	print "\n"

	colorlist = ["green", "red", "yellow", "cyan", "#eeefff"]
	for i in range(len(printlist)):
		scatter_x, scatter_y = [], []
		for index in printlist[i]:
			scatter_x.append(traindata[index].x)
			scatter_y.append(traindata[index].y)
		scatter(scatter_x, scatter_y, color=colorlist[i])
		scatter(center[i][0], center[i][1], s=150, marker="*", color="black")
	title("k_means cluster")
	show()


if __name__ == '__main__':
	global traindata
	traindata = readdata()[:]
	k1 = input("please input the cluster number: ")
	kmeans_main(k1)

