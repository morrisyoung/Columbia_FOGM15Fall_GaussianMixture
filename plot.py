## this script will load the information (either from "data" or from "result") and plot them
## the points will be colored into three different classes, and the Gaussian centers will be plotted also

import matplotlib.pyplot as plt


Z = []
Mu = []
X = []

num_point = 0
k = 0


color_list = ['y', 'g', 'r']


if __name__ == '__main__':


	print "now plot all the points with their classes and centers..."


	##=========== loading all the data ===========	
	## TODO: re-name all the files for different data to be visualized
	#file_Z = open("./data/Z.txt", 'r')
	#file_Mu = open("./data/Mu.txt", 'r')
	file_X = open("./data/X.txt", 'r')

	iter = 10
	file_Z = open("./result/iter" + str(iter) + "_Z.txt", 'r')
	file_Mu = open("./result/iter" + str(iter) + "_Mu.txt", 'r')



	# Z
	while 1:
		line = (file_Z.readline()).strip()
		if not line:
			break

		cat = int(line)
		Z.append(cat)
	print "there are",
	print len(Z),
	print "number of points"


	# Mu
	while 1:
		line = (file_Mu.readline()).strip()
		if not line:
			break

		line = line.split('\t')
		x = float(line[0])
		y = float(line[1])
		Mu.append((x, y))
	print "the centers of the",
	print k,
	print "groups are:",
	print Mu


	# X
	while 1:
		line = (file_X.readline()).strip()
		if not line:
			break

		line = line.split('\t')
		x = float(line[0])
		y = float(line[1])
		X.append((x, y))
	print "there are",
	print len(X),
	print "number of points"


	num_point = len(Z)
	k = len(Mu)

	file_Z.close()
	file_Mu.close()
	file_X.close()




	##=========== plotting ===========
	plt.figure(1)

	# points
	for i in range(num_point):
		cat = Z[i]
		color = color_list[cat]
		
		x = X[i][0]
		y = X[i][1]

		style = color + 'x'
		plt.plot([x], [y], style, alpha=0.8, markersize=5)

	# real Gaussian centers
	for i in range(k):
		cat = i
		color = color_list[cat]
		
		x = Mu[i][0]
		y = Mu[i][1]

		style = color + 'o'
		plt.plot([x], [y], style, markersize=8, label='class'+str(i))




	#plt.axis([-15, 15, -8, 4])  ## TODO: finally we can use this range
	plt.legend(numpoints=1)
	#plt.title('real grouping and the Gaussian centers')  ## TODO: change the title for the current dataset
	plt.title('learned grouping and the Gaussian centers after iter' + str(iter))


	plt.grid()
	plt.show()

