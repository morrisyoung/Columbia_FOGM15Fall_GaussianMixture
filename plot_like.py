## this script will load the information (either from "data" or from "result") and plot them
## the points will be colored into three different classes, and the Gaussian centers will be plotted also

import matplotlib.pyplot as plt



if __name__ == '__main__':


	likelihood = []
	file = open("./result/likelihood.txt", 'r')
	while 1:
		line = (file.readline()).strip()
		if not line:
			break

		value = float(line)
		likelihood.append(value)
	file.close()

	
	##=========== plotting ===========
	plt.figure(1)

	# points
	X = []
	for i in range(len(likelihood)):
		X.append(i+1)

	plt.plot(X, likelihood, 'r-o', alpha=0.8, markersize=5)


	plt.title('log likelihood curve (without all the constant terms)')
	plt.xlabel('iterations')

	plt.grid()
	plt.show()
