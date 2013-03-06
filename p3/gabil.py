import optparse
import random

# una hip siempre es una sola regla 

def parse_file(file_name):
	pass

def encode(example):
	pass

def correct_square(hipotesis, ejemplos):
	size = len(hipotesis)
	correctos = 0.0
	for ex in ejemplos:
		a = int(hipotesis[:size-2],2)
		b = int(ex[:size-2],2)
		correctos += (a&b == b) and (ex[size] == hipotesis[size])
	return corecctos**2

def compute_fitness(P):
	fitness_list = []
	for h_i in P:
		fitness_list.append(correct_square(h_i, P))
	return fitness_list

def get_total_fit(fitness_list):
	total_fitness = 0.0
	for f in fitness_list:
		total_fitness += f
	return total_fitness
		
def probabilidades(P, total_fitness):
	prob_list = []
	for i in range(P):
		prob_list.append((fitness_list[i]/total_fitness, i))
	return prob_list.sort()

def select_rueda_ruleta(P, n, total_fitness):
	PS = []
	Pr = probabilidades(P, get_total_fit(fitness_list))
	for i in range(n):
		PS.append(P[Pr[i][1]])
	return PS		


def GA(ejemplos, p, r, m):
	P = poblacion(len(ejemplos[0]), p)
	fitness_list = compute_fitness(P)
	while(1):
		n = int((1-r)*p)
		PS = select_rueda_ruleta(P, n, get_total_fit(fitness_list))
		
		

def main():
	parser = optparse.OptionParser()
	parser.add_option('-f', help='archivo de ejemplos', type='string', dest='file_name')
	parser.add_option('-p', help='tamaño de la poblacion', type='int', dest='p')
	parser.add_option('-r', help='fraccion de la pobl a reemplazarse en crossover', type='float', dest='r')
	parser.add_option('-m', help='tasa de mutacion', type='float', dest='m')
	(opts, args) = parser.parse_args()
	mandatories = ['file_name','p', 'r', 'm']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)
	ejemplos = encode(opts.file_name)
	GA(ejemplos, opts.p, opts.r, opts.m)
	
	


if __name__ == "__main__":
    main()

	
