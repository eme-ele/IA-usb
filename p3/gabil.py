import optparse
import random
import math
from encode import *


def complete_bin(size,binario):
	original_size = len(binario)
	if original_size == size:
		return binario
	for x in range(size - original_size) :
		binario = '0' + binario
	return binario

def poblacion(string_len, p):
	rule_limit = 20
	P = []
	for i in range(p):
		rule_numb = random.randint(1,rule_limit)
		new_rule = ""
		for x in range(rule_numb):
			rand = random.randint(0,2**string_len-1)
			new_rule += complete_bin(string_len, bin(rand)[2:])
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
			a = int(rule[:rule_size-1],2)
			b = int(ex[:rule_size-1],2)
			right = (a&b == b) and (ex[rule_size-1] == rule[rule_size-1])
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
	point_1 = [1,1]
	point_2 = [1,-1]
	#Crea 2 puntos aleatorios de 2 coordenadas, donde se indica la regla y la casilla respecto a la regla
	rules_numb1 = len(individuo1)/rule_size
	rules_numb2 = len(individuo2)/rule_size
	while (rules_numb2 == 1 and point_1[1] >= point_2[1] and  point_1[0] >= point_2[0]) or (rules_numb2 > 1 and point_1 >= point_2):
		point_1 = [random.randint(0,rules_numb1 -1),random.randint(0,rule_size)]
		point_2  = [random.randint(0,rules_numb1 -1),random.randint(0,rule_size)]
	point_3 = 1
	point_4 = -1
	while point_4 <= point_3:

		point_3 = [random.randint(0,rules_numb2-1),point_1[1]]
		point_4 = [random.randint(0,rules_numb2-1),point_2[1]]
	son1 = individuo1[:point_1[0]*rule_size+point_1[1]] + individuo2[point_3[0]*rule_size+point_3[1]:point_4[0]*rule_size+point_4[1]] + individuo1[point_2[0]*rule_size+point_2[1]:] 

	son2 = individuo2[:point_3[0]*rule_size+point_3[1]] + individuo1[point_1[0]*rule_size+point_1[1]:point_2[0]*rule_size+point_2[1]] + individuo2[point_4[0]*rule_size+point_4[1]:] 
	return [son1,son2]

def crossover_population(parents):
	offspring = []
	if len(parents) == 1:
		return parents

	for i in range(0,len(parents),2):
		offspring.extend(crossover(parents[i],parents[i+1]))
	#if len()
	return offspring

def mutation(individuo):
	point = random.randint(0,len(individuo)-1)
	return individuo[:point] + str(int(not int(individuo[point]))) + individuo[point+1:]


def mutate_population(PS,r):
	number = int(round(len(PS)*r))
	PS_shuffle = random.shuffle(PS)
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
				hipotesis = complete_bin(rule_size, altern_bin[2:])
		altern_PS.append(hipotesis)
	return altern_PS

def drop_cond(PS):
	drop_PS = []
	for hipotesis in PS:
		# probabilidad 0.6
		if(random.randint(1,100) <= 60):
			# escoger un atributo aleatorio para droppear
			mask = mask_atributos[random.randint(0, len(mask_atributos)-1)]
			dropped_hip = bin(int(hipotesis,2) | int(mask, 2))
			hipotesis = complete_bin(rule_size, dropped_hip[2:])
		drop_PS.append(hipotesis)
	return drop_PS


def GA(ejemplos, p, r, m):
	#print "ejemplos: " + str(ejemplos)
	P = poblacion(len(ejemplos[0]), p)
	#print "P: " + str(P)
	fitness_list = compute_fitness(P, ejemplos)
	print "fitness: " + str(fitness_list)	
	iter = 0
	fitness_old = max(fitness_list)
	fitness_new = -1
	while(fitness_new != fitness_old or iter < 30):
		fitness_old = fitness_new
		n = int(round((1-r)*p))
		#print n
		PS = weel_select(P, n, get_total_fit(fitness_list), fitness_list)
		#print "Survivor: "+ str(PS)
		n = p - n
		parents = weel_select(P, n, get_total_fit(fitness_list), fitness_list)
		#print "Parents: " + str(parents)
		offspring = crossover_population(parents)
		#print "New offspring: " + str(offspring)
		PS = PS + offspring
		#print "PS: "+str(PS)
		mutate_population(PS,m)
		#print "PS after mutation: " + str(PS)
		#PS = add_altern(PS)
		#print "add_altern con 0.01" + str(PS)
		#PS = drop_cond(PS)
		#print "drop_cond con 0.6" + str(PS)
		P = PS
		#print "P: " + str(P)
		fitness_list = compute_fitness(P, ejemplos)
		fitness_new = max(fitness_list)
		print "fitness "+ str(iter) + ":  " + str(fitness_new)
		iter += 1
	#r = P[fitness_list.index(fitness_new)]
	#print r
	#exit(-1)
	return P[fitness_list.index(fitness_new)]

		
def read_population(file_name):
	f = open(file_name)
	population = []
	for linea in f:
		if linea.strip() != '':
			population.append(linea.strip().split(","))
	return population


def create_data(population,div):
	#[0,[30,60,3000],[0,1,1000],0,0,0,0,[0,1,1000],0,0,[0,10,2000],0,0,[200,300,1000],[900,1000,10000],0]
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


def train(opts):
	population = read_population(opts.file_train)
	ejemplos = encode_population(population,data)
	global rule_size, mask_atributos
	rule_size = len(ejemplos[0])
	mask_atributos = mask_matrix(ejemplos[0],data)
	return GA(ejemplos, opts.p, opts.r, opts.m)

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
	hip = train(opts)
	print hip

	print test(opts.file_test,hip)


if __name__ == "__main__":
    main()

	
