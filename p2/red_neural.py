import optparse
import random
import math

class NeuralNetwork(object):
	"""Clase que define la estructura de red neuronal"""
	def __init__(self,  num_inputs,  num_hidden,  num_outputs):
		#pesos de la red
		self.num_inputs = num_inputs
		self.num_hidden = num_hidden
		self.num_outputs = num_outputs
		
		self.wih = random_matrix(num_inputs, num_hidden, -0.5, 0.5)
		self.who = random_matrix(num_hidden, num_outputs, -0.5, 0.5)
		#vectores de activacion de las capaz hidden y output
		self.ah = [0.0]*num_hidden
		self.ao = [0.0]*num_outputs
		#los valores de 
		self.A_wih = [[0.0]*num_hidden]*num_inputs
		self.A_who = [[0.0]*num_outputs]*num_hidden

	def propagate_forward(self, inputs):

		for h in range(self.num_hidden):
			sum = 0.0
			for i in range(self.num_inputs):
				sum += inputs[i]*self.wih[i][h]
			self.ah[h] = sigmoid(sum)

		for o in range(self.num_outputs):
			sum = 0.0
			for h in range(self.num_hidden):
				sum+= self.ah[h]*self.who[h][o]
			self.ao[o] = sigmoid(sum)
		return self.ao

	def propagate_backward(self, targets, learning_rate, momentum):
		error_out = [0.0]*self.num_outputs
		for o in range(self.num_outputs):
			error_out[o] = self.ao[o]*(1 - self.ao[o])*(targets[o] - self.ao[o])

		error_hid = [0.0]*self.num_hidden

		for h in range(self.num_hidden):
			sum = 0.0
			for o in range(self.num_outputs):
				sum += self.who[h][o]*error_out[o]
			error_hid[h] = self.ah[h]*(1 - self.ah[h])*sum

		#actualizacion
		for i in range(self.num_inputs):
			for h in range(self.num_hidden):
				self.A_wih[i][h] = learning_rate*error_hid[h]*self.ah[h] + momentum*self.A_wih[i][h]
				self.wih[i][h] = self.wih[i][h] + self.A_wih[i][h]

		for h in range(self.num_hidden):
			for o in range(self.num_outputs):
				self.A_who[h][o] = learning_rate*error_out[o]*self.ao[o] + momentum*self.A_who[h][o]
				self.who[h][o] = self.who[h][o] + self.A_who[h][o]

	def train(self, examples, learning_rate, momentum=0.1, max_iterations = 1000):

		for it in range(max_iterations):
			for e in examples:
				inputs = e[0]
				targets = e[1]
				self.propagate_forward(inputs)
				self.propagate_backward(targets,learning_rate,momentum)
			# imprime error cada 10 iteraciones
			if (it % 10 == 0):
				print "Error: " +str(self.get_error(examples))
		self.test(examples)


	def get_error(self,examples):
		error = 0.0
		for e in examples:
			input_ = e[0]
			predicted_ = self.propagate_forward(e[0])
			output_ = e[1]
			for elem in range(len(output_)):
				error += (output_[elem] - predicted_[elem])**2
		return error*0.5

	def test(self, examples):
		correct = 0
		for e in examples:
			predicted = self.propagate_forward(e[0])
			if (round(predicted[0]) == e[1][0]):
				correct += 1
			print 'Inputs:', e[0], '-->', predicted, '\tTarget', e[1]
		print "Porcentaje de clasificacion correcta: "+str(float(correct)/float(len(examples)))

def sigmoid(x):
	# evitar error en sigmoid
	if x < -709:
		x = -709
	return 1 / (1 + math.exp(-x))

def random_matrix(I,  J,  a,  b):
	matrix = []
	for i in range(I):
		fila = []
		for j in range(J):
			#inserta un elementos a la fila a insertar
			fila.append(random.uniform(a, b))
		#se inserta la fila en la matriz,  dandole la altura
		matrix.append(fila)
	return matrix

