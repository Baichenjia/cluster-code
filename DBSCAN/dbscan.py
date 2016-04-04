# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import re
from math import *
from pylab import *

def dbscan_main(eps, minpts, testdata):
	fp = open("dataset"+testdata+".txt")
	points = []
	for line in fp.readlines():
		line = line.strip()
		temp = re.split(r'\s+', line)
		points.append((float(temp[0]), float(temp[1])))
	n = len(points)
	print n
	fp.close()

	dis_eps = {}   # 字典，键为点的标号，值记录与该点距离在eps范围内的点的标号
	for i in range(n):
		dis_eps[i] = []
	for i in range(n):
		for j in range(i+1, n):
			distance = sqrt(pow((points[i][0] - points[j][0]), 2) + pow((points[i][1] - points[j][1]), 2))
			if distance < eps:
				dis_eps[i].append(j)
				dis_eps[j].append(i)
	#print dis_eps[100][:]

	#记录该点是 1：核心点 2：边界点 3：噪声点
	core_point, border_point, noise_point = [], [], []
	for i in range(n):
		#print len(dis_eps[i]),
		if len(dis_eps[i]) >= minpts:
			core_point.append(i)     # 核心点

	for i in range(n):
		if i not in core_point:
			if len(list(set(dis_eps[i]).intersection(set(core_point)))) != 0:  # 如果该点的邻近点有核心点
				border_point.append(i)  # 边界点
			else:
				noise_point.append(i)  # 噪声点

	#print
	print core_point[:]
	print border_point[:]
	print noise_point[:]

	clusters = []
	queue = []
	flag_list = [0 for i in range(n)]
	for i in range(n):
		if i in core_point:
			flag_list[i] = 0
		else:
			flag_list[i] = 2

	for p in core_point:        # 将核心点分割成簇
		newlist = []
		if flag_list[p] == 0:
			queue.append(p)
		while len(queue) != 0:
			p1 = queue.pop(0)
			flag_list[p1] = 1
			newlist.append(p1)
			for p2 in dis_eps[p1]:
				if (flag_list[p2] == 0) and (p2 not in queue) and (p2 in core_point):
					queue.append(p2)
		if len(newlist) != 0:
			clusters.append(newlist)
	#for temp in clusters:
	#	print temp[:]
	print "簇的个数 ", len(clusters)

	for p in border_point:   # 边界点归入某个核心点所在地簇中
		temp = dis_eps[p]
		maxcount = 0
		maxcluster = 0
		for index1, cluster in enumerate(clusters):
			count = len(list(set(temp).intersection(set(cluster))))  # 两个集合的交集
			if count > maxcount:
				maxcount = count
				maxcluster = index1
		clusters[maxcluster].append(p)

	#for temp in clusters:
	#	print len(temp), temp[:]

	# 绘制核心点和边界点形成的簇
	p = 0
	colorlist = ["green", "red", "gray", "cyan", "#B23AEE", "#A52A2A", "#CDBA96", "#2B2B2B"]
	for list1 in clusters:  # 循环每个组，取其中的元素
		scatter_x, scatter_y = [], []
		for pointind in list1:
			pointx, pointy = points[pointind]
			scatter_x.append(pointx)
			scatter_y.append(pointy)
		scatter(scatter_x, scatter_y, color=colorlist[p % 8])
		p += 1

	# 绘制离群点
	X1, Y1 = [], []
	for pointind in noise_point:
		pointx, pointy = points[pointind]
		X1.append(pointx)
		Y1.append(pointy)
	scatter(X1, Y1, color="black")

	#axis([0, 35, 0, 35])
	title("DBScan Cluster")
	show()

if __name__ == '__main__':
	testdata = input("please switch the dataset: ")

	if testdata == 4:
		dbscan_main(3, 5, str(testdata))
	elif testdata == 1:
		dbscan_main(5, 2, str(testdata))
	else:
		pass