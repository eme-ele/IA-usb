import red_neural
import optparse
#import ejemplo


def to_float(lista):
	lista_int = []
	for l in lista:
		lista_int.append(float(l))
	return lista_int

def generate_train(train_file):
	f = open(train_file, 'r')
	train_set = []
	for line in f:
		splitted = line.strip().split(',')
		splitted_int = to_float(splitted)
		example = []
		example.append(splitted_int[:6])
		# modifica salida de 2/1 a 1/0		
		if (splitted_int[6]==2):
			example.append([1.0])
		else:
			example.append([0.0])
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
	network = red_neural.NeuralNetwork(6, opts.num_hidden, 1)
	network.train(pat, opts.learning_rate)


if __name__ == "__main__":
	main()

