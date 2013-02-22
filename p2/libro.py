import math
import optparse
import random

class NeuralNetwork():	
	def __init__(self, num_inputs, num_hidden, num_outputs):
		self.ni = num_inputs  #+1 bias
		self.nh = num_hidden
		self.no = num_outputs
		# salidas de las tres capas
		self.ah = [1.0]*self.nh
		self.ao = [1.0]*self.no
		# pesos de las capas hidden y output
		self.wh = random_matrix(self.ni, self.nh, -0.5, 0.5)
		self.wo = random_matrix(self.nh, self.no, -0.5, 0.5)
		# ultima varacion de los pesos de las capas hidden y output
		self.vh_last = fill_matrix(self.ni, self.nh, 0.0)
		self.vo_last = fill_matrix(self.nh, self.no, 0.0)

	def propagate_forward(self, inputs):
		# propagar de input a hidden
		for j in range(self.nh):
			sum = 0.0
			for i in range(self.ni):
				sum += (inputs[i] * self.wh[i][j])
			self.ah[j] = sigmoid(sum)
		# propagar de hidden a output
		for k in range(self.no):
			sum = 0.0
			for j in range(self.nh):
				sum += (self.ah[j] + self.wo[j][k])
			self.ao[k] = sigmoid(sum)
		return self.ao

	def propagate_backward(self, target, inputs, learning_rate):
		#calcular error para cada neurona output
		delta_k = [0.0]*self.no
		for k in range(self.no):
			delta_k[k] = self.ao[k]*(1-self.ao[k])*(target[k]-self.ao[k])

		# calcular error para cada neurona hidden
		delta_h = [0.0]*self.nh
		for j in range(self.nh):
			sum = 0.0
			for k in range(self.no):
				sum += self.wh[j][k]*delta_k[k]
			delta_h[j] = self.ah[j]*(1-self.ah[j])*sum

		#actualizar pesos en capa output
		for j in range(self.nh):
			for k in range(self.no):
				variation = learning_rate*delta_k[k]*self.ah[j]
				self.wo[j][k] = self.wo[j][k] + variation

		#actualizar pesos en capa hidden
		for i in range(self.ni):
			for j in range(self.nh):
				variation = learning_rate*delta_h[j]*inputs[i]
				self.wh[i][j] = self.wh[i][j] + variation

	def test(self, patterns):
		for p in patterns:
			inputs = p[0]
	 		print 'Inputs:', p[0], '-->', self.propagate_forward(inputs), '\tTarget', p[1]


def random_matrix(I, J, a, b):
	matrix = []
	for i in range(I):
		line = []
		for j in range(J):
			line.append(random.uniform(a,b))
		matrix.append(line)
	return matrix

def fill_matrix(I, J, fill):
	matrix = []
	for i in range(I):
		line = []
		for j in range(J):
			line.append(fill)
		matrix.append(line)
	return matrix

def sigmoid(x):
	return 1 / (1 + math.exp(-x))

def dv_sigmoid(x):
	return sigmoid(x)*(1-sigmoid(x))

def backpropagation(examples, learning_rate, num_inputs, num_hidden, num_outputs, max_iterations=1000):
	network = NeuralNetwork(num_inputs, num_hidden, num_outputs)
	for i in range(max_iterations):
		for e in examples:
			inputs = e[0]
			target = e[1]
			network.propagate_forward(inputs)
			network.propagate_backward(target, inputs, learning_rate)
	network.test(examples)

def main():
	# parse input options
	parser = optparse.OptionParser()
	parser.add_option('-i', help='number of inputs', type='int', dest='num_inputs')
	parser.add_option('-n', help='number of hidden layer neurons', type='int', dest='num_hidden')
	parser.add_option('-l', help='learning rate', type='float', dest='learning_rate')	
	(opts, args) = parser.parse_args()
	mandatories = ['num_inputs', 'num_hidden', 'learning_rate']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Mandatory option missing"
			parser.print_help()
			exit(-1)

	xor = [
		[[0,0], [1]],
		[[0,1], [1]], 
		[[1,0], [1]],
		[[1,1], [0]]
	]
	backpropagation(xor, opts.learning_rate, opts.num_inputs, opts.num_hidden, 1)

if __name__ == "__main__":
	main()


