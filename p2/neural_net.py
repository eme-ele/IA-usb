import math
import optparse
import random
import string

class NeuralNetwork():	
	def __init__(self, num_inputs, num_hidden, num_outputs):
		self.ni = num_inputs+1 #+1 bias
		self.nh = num_hidden
		self.no = num_outputs
		# salidas de las tres capas
		self.ai = [1.0]*self.ni
		self.ah = [1.0]*self.nh
		self.ao = [1.0]*self.no
		# pesos de las capas hidden y output
		self.wh = random_matrix(self.ni, self.nh, -0.2, 0.2)
		self.wo = random_matrix(self.nh, self.no, -0.2, 0.2)
		# ultima varacion de los pesos de las capas hidden y output
		self.vh_last = fill_matrix(self.ni, self.nh, 0.0)
		self.vo_last = fill_matrix(self.nh, self.no, 0.0)

	def propagate_forward(self, inputs):
		for i in range(self.ni-1):
			self.ai[i] = inputs[i]
		# propagar de input a hidden
		for j in range(self.nh):
			sum = 0.0
			for i in range(self.ni):
				sum += (self.ai[i] * self.wh[i][j])
			self.ah[j] = sigmoid(sum)
		# propagar de hidden a output
		for k in range(self.no):
			sum = 0.0
			for j in range(self.no):
				sum += (self.ah[j] + self.wo[j][k])
			self.ao[k] = sigmoid(sum)
		return self.ao

	def propagate_backward(self, target, learning_rate):
		#calcular error para cada neurona output
		delta_k = [0.0]*self.no
		for k in range(self.no):
			delta_k[k] = dv_sigmoid(self.ao[k])*(target[k]-self.ao[k])

		#actualizar pesos en capa output
		for j in range(self.nh):
			for k in range(self.no):
				change = delta_k[k]*self.ah[j]
				self.wo[j][k] = learning_rate*self.vo_last[j][k] + 0.1*change
				self.vo_last[j][k] = change

		# calcular error para cada neurona hidden
		delta_h = [0.0]*self.nh
		for j in range(self.nh):
			sum = 0.0
			for k in range(self.no):
				sum += self.wo[j][k]*delta_k[k]
			delta_h[j] = dv_sigmoid(self.ah[j])*sum

		#actualizar pesos en capa hidden
		for i in range(self.ni):
			for j in range(self.nh):
				change = delta_h[j]*self.ai[i]
				self.wh[i][j] = learning_rate*self.vh_last[i][j] + 0.1*change
				self.vh_last[i][j] = change

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
	return math.tanh(x)
	#return 1 / (1 + math.exp(-x))

def dv_sigmoid(y):
	return 1 - y**2
	#return sigmoid(x)*(1-sigmoid(x))

def backpropagation(examples, learning_rate, num_inputs, num_hidden, num_outputs, max_iterations=1000):
	network = NeuralNetwork(num_inputs, num_hidden, num_outputs)
	for i in range(max_iterations):
		for e in examples:
			inputs = e[0]
			target = e[1]
			network.propagate_forward(inputs)
			network.propagate_backward(target, learning_rate)
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


