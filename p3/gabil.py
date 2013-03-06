import optparse
import random

# una hip siempre es una sola regla 

def parse_file(file_name):
	pass

def encode(example):
	pass

def complete_bin(size,binario):
	original_size = len(binario)
	if original_size == size:
		return binario
	for x in range(size - original_size) :
		binario = '0' + binario
	return binario

def poblacion(string_len, p):
	P = []
	for i in range(p):
		rand = random.randint(0,2**string_len-1)
		P.append(complete_bin(string_len, bin(rand)[2:]))
	return P

def correct_square(hipotesis, ejemplos):
	size = len(hipotesis)
	correctos = 0
	for ex in ejemplos:
		a = int(hipotesis[:size-2],2)
		b = int(ex[:size-2],2)
		correctos += (a&b == b) and (ex[size-1] == hipotesis[size-1])
	return correctos**2

def compute_fitness(P, ejemplos):
	fitness_list = []
	for h_i in P:
		fitness_list.append(correct_square(h_i, ejemplos))
	return fitness_list

def get_total_fit(fitness_list):
	total_fitness = 0.0
	for f in fitness_list:
		total_fitness += f
	return total_fitness
		
def probabilidades(P, total_fitness, fitness_list):
	prob_list = []
	prob = 0.0
	for i in range(len(P)):
		if (total_fitness != 0):
			prob = fitness_list[i]/total_fitness
		pair = (prob, i)
		prob_list.append(pair)
	return sorted(prob_list)	

def select_rueda_ruleta(P, n, total_fitness, fitness_list):
	PS = []
	Pr = probabilidades(P, total_fitness, fitness_list)
	for i in range(n):
		PS.append(P[Pr[i][1]])
	return PS		


def GA(ejemplos, p, r, m):
	print "ejemplos: " + str(ejemplos)
	P = poblacion(len(ejemplos[0]), p)
	print "P: " + str(P)
	fitness_list = compute_fitness(P, ejemplos)
	while(1):
		n = int(round((1-r)*p))
		PS = select_rueda_ruleta(P, n, get_total_fit(fitness_list), fitness_list)
		print "PS: "+ str(PS)
		exit(-1)
		
		

def main():
	parser = optparse.OptionParser()
	parser.add_option('-f', help='archivo de ejemplos', type='string', dest='file_name')
	parser.add_option('-p', help='tamano de la poblacion', type='int', dest='p')
	parser.add_option('-r', help='fraccion de la pobl a reemplazarse en crossover', type='float', dest='r')
	parser.add_option('-m', help='tasa de mutacion', type='float', dest='m')
	(opts, args) = parser.parse_args()
	mandatories = ['file_name','p', 'r', 'm']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)
	#ejemplos = encode(opts.file_name)
	ejemplos = ['10101', '10011', '01101', '01010']
	GA(ejemplos, opts.p, opts.r, opts.m)
	
	


if __name__ == "__main__":
    main()

	
