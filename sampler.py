## this is the main script for Gibbs sampling
## we will set the maximum sampling numbers
## we will save the current results every INTERVAL interations, and these intermediate results will be plotted later on; we need to set INTERVAL
## we will print out and also save the current log joint likelihood for the whole sampling process, to monitor the convergence

import numpy as np


Z = []
Mu = []
X = []

num_point = 0
k = 0


sigma = 1.0
lamb = 2.0


iteration = 20




def result_save(iter):
	global Z
	global Mu

	##=========== save all the data we just learned ===========
	# Z
	file = open("./result/iter" + str(iter) + "_Z.txt", 'w')
	for i in range(len(Z)):
		cat = Z[i]
		file.write(str(cat) + "\n")
	file.close()

	# Mu
	file = open("./result/iter" + str(iter) + "_Mu.txt", 'w')
	for i in range(len(Mu)):
		x = Mu[i][0]
		y = Mu[i][1]
		file.write(str(x) + "\t" + str(y) + "\n")
	file.close()

	return




if __name__ == '__main__':


	##=========== loading X, and initializing Z and Mu ===========
	print "loading the data X, and initializing Mu and Z..."

	file_Mu = open("./data/Mu.txt", 'r')
	file_X = open("./data/X.txt", 'r')

	# X
	while 1:
		line = (file_X.readline()).strip()
		if not line:
			break

		line = line.split('\t')
		x = float(line[0])
		y = float(line[1])
		X.append((x, y))
	num_point = len(X)


	# Mu
	while 1:
		line = (file_Mu.readline()).strip()
		if not line:
			break

		line = line.split('\t')
		x = float(line[0])
		y = float(line[1])
		Mu.append([x, y])
	k = len(Mu)
	Mu = []
	## initialize some new centers
	list = np.random.normal(0, lamb * lamb, k * 2)
	for i in range(k):
		Mu.append([list[2 * i], list[2 * i + 1]])


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



	##=========== Gibbs sampling ===========
	print "now start sampling (we will show the trend of the log joint likelihood)"


	file = open("./result/likelihood.txt", 'w')

	for i in range(iteration):
		print "iter#",
		print i+1,

		# Z
		for j in range(num_point):  # for Z[j], a 0/1/2 indicator
			x = X[j][0]
			y = X[j][1]

			# TODO: now we treat the Cat distribution has equal probability distribution across all the cats
			#		so now the complete conditional distribution is only related to the likelihood given the Gaussian center

			# get three Gaussian values: (we drop the items outside exponential)
			# TODO: here we fix the number of mixtures is 3
			like1 = np.exp( - (np.square(Mu[0][0] - x) + np.square(Mu[0][1] - y)) / (2 * sigma * sigma) )
			like2 = np.exp( - (np.square(Mu[1][0] - x) + np.square(Mu[1][1] - y)) / (2 * sigma * sigma) )
			like3 = np.exp( - (np.square(Mu[2][0] - x) + np.square(Mu[2][1] - y)) / (2 * sigma * sigma) )
			sum = like1 + like2 + like3
			prob1 = like1 / sum
			prob2 = like2 / sum
			prob3 = like3 / sum

			## generate the current z from Cat distribution
			cat_prob_list = [prob1, prob2, prob3]
			list = np.random.multinomial(1, cat_prob_list, size=None)
			cat = 0  # 0, 1, ..., k-1
			for m in range(k):
				if list[m] == 1:
					cat = m
					break
			Z[j] = cat

		# Mu
		for j in range(k):  # for Mu[j], a (x, y) coordinate
			nk = 0
			for m in range(num_point):
				if Z[m] == j:
					nk += 1

			# for (x, y), or (Mu[j][0], Mu[j][1])
			xk_bar = 0
			yk_bar = 0
			for m in range(num_point):
				if Z[m] == j:
					xk_bar += X[m][0]
					yk_bar += X[m][1]
			xk_bar = xk_bar / (nk * 1.0)
			yk_bar = yk_bar / (nk * 1.0)
			temp1 = nk / np.square(sigma)
			temp2 = 1 / np.square(lamb)
			muk_bar_x = ( temp1 / ( temp1 + temp2 ) ) * xk_bar
			muk_bar_y = ( temp1 / ( temp1 + temp2 ) ) * yk_bar
			lamb_bar = 1 / ( temp1 + temp2 )
			# draw x and y in N(muk_bar_x/y, lamb_bar)
			Mu[j][0] = np.random.normal(muk_bar_x, np.sqrt(lamb_bar), 1)[0]
			Mu[j][1] = np.random.normal(muk_bar_y, np.sqrt(lamb_bar), 1)[0]


		# log likelihood (I will ignore all the constant items)
		likelihood = 0
		# Z relevant is ignored, as the Cat has an equal probability distribution
		#
		#
		#
		# Mu: the log-constant can be ignored, and we only have the square (mimus) term
		for j in range(k):
			likelihood += ( - (np.square(Mu[j][0]) + np.square(Mu[j][1])) / (2 * lamb * lamb) )
		# X | Z, Mu: again, the log-constant can be ignored, and there is only the square (minus) term
		for j in range(num_point):
			x = X[j][0]
			y = X[j][1]
			cat = Z[j]
			likelihood += ( - (np.square(Mu[cat][0] - x) + np.square(Mu[cat][1] - y)) / (2 * sigma * sigma) )

		print "current log likelihood is (without constant terms)",
		print likelihood


		# parameter saving
		file.write(str(likelihood) + '\n')
		result_save(i+1)


	print "now finish Gibbs sampling..."


	file.close()



