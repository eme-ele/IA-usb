import optparse
import random
import math
from encode import *
import sys

def complete_bin(size,binario):
	original_size = len(binario)
	if original_size == size:
		return binario
	for x in range(size - original_size) :
		binario = '0' + binario
	return binario

def poblacion(string_len, p):
	rule_limit = 3
	P = []
	for i in range(p):
		rule_numb = random.randint(2,rule_limit)
		new_rule = ""
		for x in range(rule_numb):
			rand = random.randint(0,2**string_len-1)
			new_rule += complete_bin(string_len, bin(rand)[2:])
		if len(new_rule)%60 !=0:
			print "ERROR poblacion_aleatoria"
			print "tamano: " + str(len(new_rule))
			exit(-1)
		P.append(new_rule)
	
	return P


def correct_square(hipotesis, ejemplos):
	size = len(hipotesis)
	rules = [hipotesis[i:i+rule_size] for i in range(0,size,rule_size)]
	correctos = 0
	if len(rules) > 5:
		return 0
	for ex in ejemplos:
		right = 1
		for rule in rules:
			try:	
				a = int(rule[:rule_size-1],2)
				b = int(ex[:rule_size-1],2)
				right = (a&b == b) and (ex[rule_size-1] == rule[rule_size-1])
			except:
				print "ERROR - correct_square"
				print "Rules: " + str(rules)
				print "Ejemplo: "+ str(ex)
				print "Long de rule: " + str(len(rule))
				print "Long de Ejemplo: " + str(len(ex))
				print "Long de Hipotesis: " + str(len(hipotesis))
				print "Rule_size: " + str(rule_size)
				exit(-1)
			if not right:
				break
		correctos += right
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
	return sorted(prob_list,reverse=True)	

def weel_select(P, n, total_fitness, fitness_list):
	PS = []
	Pr = probabilidades(P, total_fitness, fitness_list)
	sum = 0
	for elem in Pr:
		sum += elem[0]
	for i in range(n):
		lanzamiento = random.random()*sum
		circle = 0
		for e in range(len(Pr)):
			circle += Pr[e][0]
			if lanzamiento <= circle:
				PS.append(P[Pr[e][1]])
				break
	return PS			


def tournament_select(P, n, total_fitness, fitness_list):
	k = 2
	PS = []
	best = 0.0
	choice_index = 0
	for i in range(n):
		for j in range(k):
			index = random.randint(0, len(fitness_list)-1)
			if (fitness_list[index] > best):
				best = fitness_list[index]
				choice_index = index
		PS.append(P[choice_index])
	return PS


def crossover(individuo1,individuo2):

	#rule_size
	while(True):
		point_1 = random.randint(0,len(individuo1)-1)
		point_2 = random.randint(point_1,len(individuo1)-1)
		d1 = point_1%rule_size
		d2 = point_2%rule_size
		
		if len(individuo2) != rule_size or d2>d1:
			break
	while(True):
		point_3 = random.randint(0,len(individuo2)/rule_size - 1)*rule_size + d1
		point_4 = random.randint(0,len(individuo2)/rule_size - 1)*rule_size + d2
		if point_3<=point_4:
			break

	son1 = individuo1[:point_1] + individuo2[point_3:point_4] + individuo1[point_2:]
	son2 = individuo2[:point_3] + individuo1[point_1:point_2] + individuo2[point_4:]
	if len(son1)%60 != 0:
		print "ERROR crossover son1"
		exit(-1)
	if len(son2)%60 != 0:
		print "ERROR crossover son2"
		exit(-1)


	return [son1,son2]

def crossover_population(parents):
	offspring = []
	if len(parents) == 1:
		return offspring
	l = len(parents)
	if l%2 != 0:
		l-=1
	for i in range(0,l,2):
		offspring.extend(crossover(parents[i],parents[i+1]))
	#if len()
	return offspring

def mutation(individuo):
	point = random.randint(0,len(individuo)-1)
	res = individuo[:point] + str(int(not int(individuo[point]))) + individuo[point+1:]
	if len(res)%60 != 0:
		print "ERROR mutation"
		print individuo
		print res
		exit(-1)
	return res


def mutate_population(PS,r):
	number = int(round(len(PS)*r))
	random.shuffle(PS)
	for individuo in range(number):
		PS[individuo] = mutation(PS[individuo])
	


def make_mask(pos, length):
	mask = ''
	for i in range(length):
		if i == pos:
			mask += '1'
		else:
			mask += '0'
	return mask

def add_altern(PS):
	altern_PS = []
	for hipotesis in PS:
		# probabilidad 0.01
		if(random.randint(1, 100) == 1):
			# ver donde hay ceros en los atributos y elegir uno aleatorio para alterar
			cero_pos = []
			for i in range(len(hipotesis)-1):
				if hipotesis[i] == '0':
					cero_pos.append(i)
			if (len(cero_pos)>0):
				mask = make_mask(cero_pos[random.randint(0, len(cero_pos)-1)], len(hipotesis))
				altern_bin =  bin(int(hipotesis,2) | int(mask, 2))
				hipotesis = complete_bin(len(hipotesis), altern_bin[2:])
				if len(hipotesis)%60 != 0:
					print "ERROR addicionar alternavo"
					print len(hipotesis)
					print len(mask)
					print altern_bin
					exit(-1)
		altern_PS.append(hipotesis)
	return altern_PS

def drop_cond(PS):
	drop_PS = []
	for hipotesis in PS:
		# probabilidad 0.6
		if(random.randint(1,100) <= 60):
			size = len(hipotesis)
			rules = [hipotesis[i:i+rule_size] for i in range(0,size,rule_size)]
			# escoger aleatoriamente la regla a modificar
			chosen_rule = random.randint(0, len(rules)-1)
			# escoger un atributo aleatorio para droppear
			att = random.randint(0, len(mask_atributos)-1)
			mask = ((chosen_rule*rule_size)*'0') + mask_atributos[att] + (((len(rules)-1-chosen_rule)*rule_size)*'0')
			dropped_hip = bin(int(hipotesis,2) | int(mask, 2))
			hipotesis = complete_bin(size, dropped_hip[2:])
			if len(hipotesis)%60 != 0:
				print "ERROR drop_cond"
				print len(hipotesis)
				print len(mask)
				print dropped_hip
				exit(-1)
		drop_PS.append(hipotesis)
	return drop_PS


def GA(ejemplos, p, r, m,weelPS,weelParent):
	#print "ejemplos: " + str(ejemplos)
	P = poblacion(len(ejemplos[0]), p)
	#print "P: " + str(P)
	fitness_list = compute_fitness(P, ejemplos)
	#print "fitness: " + str(fitness_list)	
	iter = 0
	fitness_old = max(fitness_list)
	fitness_new = -1
	while(fitness_new < 88209 and iter < 100):
		fitness_old = fitness_new
		n = int(round((1-r)*p))
		#print n
		if weelPS:
			PS = weel_select(P, n, get_total_fit(fitness_list), fitness_list)
		else:
			PS = tournament_select(P, n, get_total_fit(fitness_list), fitness_list)
		#print "Survivor: "+ str(PS)
		n = p - n
		if weelParent:
			parents = weel_select(P, n, get_total_fit(fitness_list), fitness_list)
		else:
			parents = tournament_select(P, n, get_total_fit(fitness_list), fitness_list)
		#print "Parents: " + str(parents)
		offspring = crossover_population(parents)
		#print "New offspring: " + str(offspring)
		PS = PS + offspring
		#print "PS:                " + str(PS)
		mutate_population(PS,m)
		#print "PS after mutation: " + str(PS)
		PS = add_altern(PS)
		#print "add_altern con 0.01" + str(PS)
		PS = drop_cond(PS)
		#print "drop_cond con 0.6" + str(PS)
		P = PS
		#print "P: " + str(P)
		fitness_list = compute_fitness(P, ejemplos)
		fitness_new = max(fitness_list)
		print str(iter)+": "+str(fitness_new)
		#sys.stdout.write("\r\rfitness "+ str(iter+1) + ":  " + str(fitness_new) + "\n")
		iter += 1
	#r = P[fitness_list.index(fitness_new)]
	#print r
	#exit(-1)
	return iter,P[fitness_list.index(fitness_new)],fitness_new

		
def read_population(file_name):
	f = open(file_name)
	population = []
	for linea in f:
		if linea.strip() != '':
			population.append(linea.strip().split(","))
	return population


def create_data(population,div):
	data = []
	div_list = [0,div[0],div[1],0,0,0,0,div[2],0,0,div[3],0,0,div[4],div[5],0]
	for b in range(len(div_list)):
		if div_list[b]:
			temp = []
			for p in population:
				if p[b] != "?":
					temp.append(float(p[b]))
			data.append([min(temp),max(temp),div_list[b]])
		else:
			data.append(0)
	#for row in range(len(data)):
		

	return data


def train(opts,weelPS,weelParent):
	population = read_population(opts.file_train)
	ejemplos = encode_population(population,data)
	global rule_size, mask_atributos
	rule_size = len(ejemplos[0])
	mask_atributos = mask_matrix(ejemplos[0],data)
	return GA(ejemplos, opts.p, opts.r, opts.m,weelPS,weelParent)

def test(file_name,hipotesis):
	population = read_population(file_name)
	ejemplos = encode_population(population,data)
	return math.sqrt(correct_square(hipotesis,ejemplos))/float(len(ejemplos))
	


def main():
	parser = optparse.OptionParser()
	parser.add_option('-e', help='archivo de entrenamiento', type='string', dest='file_train')
	parser.add_option('-t', help='archivo de prueba', type='string', dest='file_test')
	parser.add_option('-p', help='tamano de la poblacion', type='int', dest='p')
	parser.add_option('-r', help='fraccion de la pobl a reemplazarse en crossover', type='float', dest='r')
	parser.add_option('-m', help='tasa de mutacion', type='float', dest='m')
	(opts, args) = parser.parse_args()
	mandatories = ['file_train','file_test','p', 'r', 'm']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)


	#data debe crearse con un vector de numero de intervalos. Cada uno representaria el numero de divisiones del elemento i del rasgo continuo
	div = 26
	global data
	data = [0,[13.75,80.25,div],[0,28,div],0,0,0,0,[0,28.5,div],0,0,[0,67,div],0,0,[0,2000,div],[0,100000,div],0]
	#ejemplos = encode(opts.file_name)
	#global rule_size, mask_atributos
	# luego hay que cambiarlos para los ejemplos dados
	#rule_size = 0
	
	for primer in range(2):
		for segundo in range(2):
			fitness_acum = 0.0
			iter_acum = 0.0
			accuracy_acum = 0.0		
			print "Caso: " + str(primer*2 + segundo)
			if primer:
				print "		Weel PS"
			else:
				print "		Tournament PS"
			if segundo:
				print "		Weel Parents"
			else:
				print "		Tournament Parents"
			for x in range(10):
				it,hip,fitness = train(opts,primer,segundo)
				print "Hipotesis Resultante: " + hip
				accuracy_acum+= test(opts.file_test,hip)
				fitness_acum+=fitness
				iter_acum += it
			print "Promedios:"
			print "		Accuracy: 	" + str(accuracy_acum/10.0)
			print "		Fitness:  	" + str(fitness_acum/10.0)
			print "		Iteration:	" + str(iter_acum/10.0)


if __name__ == "__main__":
    main()

	
