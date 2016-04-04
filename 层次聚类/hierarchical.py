# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

from pylab import *
import collections
from math import *
import re

def hierar_min(n):
	# 读取数据点
	fp = open("dataset2.txt")
	points = []
	for line in fp.readlines():
		line = line.strip()
		point = re.split(r'\s+', line)
		#print point[:]
		points.append((float(point[0]), float(point[1])))

	# 初始化簇，存储每个簇所属的类标号
	group = []
	for index in range(len(points)):
		group.append(index)

	# 初始化两点间的距离矩阵，用字典表示，键为两个点的序号，值为两个点之间的距离
	dis_matrix = {}
	for idx1, point1 in enumerate(points):  # 顺序遍历，返回点的序号和坐标
		for idx2, point2 in enumerate(points):
			if idx1 < idx2:
				dis = sqrt(pow((point1[0] - point2[0]), 2) + pow((point1[1] - point2[1]), 2))
				keystr = str(idx1) + '#' + str(idx2)
				dis_matrix[keystr] = dis

	# 对字典按照距离大小排序 按值排序
	dis_matrix = collections.OrderedDict(sorted(dis_matrix.items(), key=lambda t: -t[1]))

	#for key, value in dis_matrix.iteritems():
	#	print key, value

	group_num = len(group)
	while True:
		keystr, dis = dis_matrix.popitem()  # 获取当前dis最小的点
		keystr_list = re.split(r'#', keystr)
		point1_index = int(keystr_list[0])
		point2_index = int(keystr_list[1])  # 两个点的序号

		# 如果它们不在同一个簇中则合并
		if group[point1_index] != group[point2_index]:
			group1 = group[point1_index]
			group2 = group[point2_index]
			for val in range(len(group)):  # 将当前标号为第二组时标记为第一组
				if group[val] == group2:
					group[val] = group1
			group_num -= 1

		#对当前组内还有多少个不同的元素进行统计  有多少个不同元素就代表有多少组
		commonlist = collections.Counter(group).most_common()
		#print len(commonlist)
		if len(commonlist) == n:  # 如果达到了用户指定的簇的个数则停止层次聚类
			break

	# 对点进行分组，分入指定的簇中
	set_group = set(group)
	set_group = list(set_group)
	resultlist = []
	for i in range(len(set_group)):
		resultlist.append([])
	for point_ind in range(len(group)):
		temp = group[point_ind]   # 该点所属类别
		temp1 = set_group.index(temp)  # 该类别对应的set_group的序号
		resultlist[temp1].append(point_ind)  # 将该点存入相应的list中去

	# 绘图
	p = 0
	colorlist = ["green", "red", "gray", "cyan", "#B23AEE", "#A52A2A", "#CDBA96", "#2B2B2B"]
	for list1 in resultlist:  # 循环每个组，取其中的元素
		scatter_x, scatter_y = [], []
		for pointind in list1:
			pointx, pointy = points[pointind]
			scatter_x.append(pointx)
			scatter_y.append(pointy)
		scatter(scatter_x, scatter_y, color=colorlist[p % 8])
		p += 1
	title("hierachical cluster")
	show()




if __name__ == "__main__":
	n = input("please input the number of cluster when end the hierarchical cluster: ")
	hierar_min(n)