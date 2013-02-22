import redTeorica
import optparse
import ejemplo

def to_int(lista):
	lista_int = []
	for l in lista:
		lista_int.append(float(l))
	return lista_int

def generate_train(train_file):
	f = open(train_file, 'r')
	train_set = []
	for line in f:
		splitted = line.strip().split()
		print splitted
		splitted_int = to_int(splitted)
		example = []
		example.append(splitted_int[:2])
		example.append(splitted_int[2:])
		#print example
		train_set.append(example)
	return train_set


def main():
	# parse input options
	parser = optparse.OptionParser()
	parser.add_option('-n', help='number of hidden layer neurons', type='int', dest='num_hidden')
	parser.add_option('-l', help='learning rate', type='float', dest='learning_rate')	
	parser.add_option('-t', help='training file', type='string', dest='train_file')
	(opts, args) = parser.parse_args()
	mandatories = ['train_file', 'num_hidden', 'learning_rate']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Mandatory option missing"
			parser.print_help()
			exit(-1)

	pat = generate_train(opts.train_file)
	network = redTeorica.NeuralNetwork(2, opts.num_hidden, 1)
	network.train(pat, opts.learning_rate)
	#network = ejemplo.NN(2, opts.num_hidden, 1)
	#network.train(pat)



if __name__ == "__main__":
	main()

