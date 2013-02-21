import optparse
import math

class Neuron():	
	def __init__(self, length):
		self.n = lenght
		self.weights = init_weights(length);
		self.last_delta = [0.0]*(length)
	
	def activate(self, activations):
		sum = 0.0
		for i in range(self.n):
			sum += (activations[i] * self.weights[i])
		return sum	

	def update_weights(self, deriv, activation):
		for i in range(self.n):
			delta = deriv[i] * activation 
			self.weights[i] += delta + self.last_delta[i]
			self.last_delta[i] = delta
	
			

class NeuralNetwork():	
	def __init__(self, num_inputs, num_hidden, num_outputs):
		self.ni = num_inputs+1  #+1 bias
		self.nh = num_hidden
		self.no = num_outputs
		# activaciones
		self.ai = [1.0]*self.ni
		self.ah = [1.0]*self.nh
		self.ao = [1.0]*self.no
		# capas
		self.li = [Neuron(self.nh)]*self.ni
		self.lh = [Neuron(self.no)]*self.nh

	def forward_propagate(self, inputs):
		for i in range(self.ni):
			self.ai[i] = inputs[i]
		for j in range(self.nh):
			self.ah[j] = sigmoid(li[j].activate(ai))
		for k in range(self.no):
			self.ao[k] = sigmoid(lh[k].activate(ah))

	def back_propagate(self, targets):
		output_deriv = [0.0]*self.no
		hidden_deriv = [0.0]*self.nh

		# calcular output deriv
		for k in range(self.no):
			error = targets[k] - self.ao[k] 
			output_deriv[k] = error * dsigmoid(self.ao[l])

		# actualizar pesos de salida
		for j in range(self.nh):
			lh[j].update_weights(output_deriv, self.ah)

		# calcular hidden deriv
		for j in range(self.nh):
			error = 0.0
			for k in range(self.no):
				error += output_deriv * self.lh[j].weights[k]
			hidden_deriv[j] = error * dsigmoid(self.ah[j])

		# actualizar pesos internos
		for i in range(self.ni):
			li[i].update_weights(hidden_deriv, self.ai)

	
	def train(self, examples, max_iterations=1000):
		correct = 0
		for i in range(max_iterations):
			for e in examples:
				inputs = e[0]
				targets = e[1]
				self.forward_propagate(inputs)
				self.back_propagate(targets)			
		

def init_weights(num_inputs):
	w = []
	for i in range(num_inputs):
		w.append(random.uniform(0, 0.5))
	return w

def sigmoid(activation):
	return 1.0 / (1.0 + exp(-activation))


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

	network = NeuralNetwork(opts.num_inputs, opts.num_hidden, 1)
	network.train(xor)
	
#	(xor, opts.num_inputs, opts.iterations, opts.num_hidden, opts.learning_rate)	


if __name__ == "__main__":
	main()
