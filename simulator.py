## this script will generate the points from the Gaussian mixture model
## the mixtures (points, belongings, and Gaussian centers) will be saved in the "./data" folder
## the simulated data will be loaded into "sampler.py" program in a later stage, but the belongings and the Gaussian centers will be ignored


import numpy as np


num_point = 1000
k = 3

sigma = 1.0
lamb = 2.0

Mu = []
Z = []
X = []



if __name__ == '__main__':


	print "now generating the Gaussian mixture..."

	##=========== initialize all the containers ===========
	# Z
	cat_prob_list = [1/(k * 1.0)] * k
	for i in range(num_point):
		## generate the z from Cat distribution
		list = np.random.multinomial(1, cat_prob_list, size=None)
		cat = 0  # 0, 1, ..., k-1
		for i in range(k):
			if list[i] == 1:
				cat = i
				break
		Z.append(cat)

	# Mu
	list = np.random.normal(0, lamb * lamb, k * 2)
	for i in range(k):
		Mu.append((list[2 * i], list[2 * i + 1]))

	# X
	for i in range(num_point):
		cat = Z[i]
		x = np.random.normal(Mu[cat][0], sigma * sigma, 1)[0]
		y = np.random.normal(Mu[cat][1], sigma * sigma, 1)[0]
		X.append((x, y))


	##=========== save all the data we just simulated ===========
	# Z
	file = open("./data/Z.txt", 'w')
	for i in range(len(Z)):
		cat = Z[i]
		file.write(str(cat) + "\n")
	file.close()

	# Mu
	file = open("./data/Mu.txt", 'w')
	for i in range(len(Mu)):
		x = Mu[i][0]
		y = Mu[i][1]
		file.write(str(x) + "\t" + str(y) + "\n")
	file.close()

	# X
	file = open("./data/X.txt", 'w')
	for i in range(len(X)):
		x = X[i][0]
		y = X[i][1]
		file.write(str(x) + "\t" + str(y) + "\n")
	file.close()



	print "simulation done, all data saved into ./data directory..."
