import optparse
import random
import math
from encode import *

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
	return sorted(prob_list,reverse=True)	

def weel_select(P, n, total_fitness, fitness_list):
	PS = []
	Pr = probabilidades(P, total_fitness, fitness_list)
	#print P
	#print total_fitness
	#print fitness_list
	#print Pr
	#print "\n\n\n\n"
	for i in range(n):

		lanzamiento = random.random()
		circle = 0
		#print len(PS)
		#print "El lanzamiento fue de:" + str(lanzamiento)
		#print i
		for e in range(len(Pr)):
			circle += Pr[e][0]
			#print " 	Es menor que " + str(circle) + " ?"
			if lanzamiento <= circle:
				PS.append(P[Pr[e][1]])
				#Pr.remove(Pr[e])
				break
			#print " 	No por ahora"
	#print PS
	#exit(-1)
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
	point_1 = 1
	point_2 = -1
	#Crea 2 puntos aleatorios de 2 coordenadas, donde se indica la regla y la casilla respecto a la regla
	while point_1 >= point_2:
		point_1 = (random.randint(0,len(individuo1)/rule_size -1),random.randint(0,rule_size))
		point_2 = (random.randint(0,len(individuo1)/rule_size -1),random.randint(0,rule_size))
	point_3 = 1
	point_4 = -1
	while point_4 <= point_3:
		point_3 = [random.randint(0,len(individuo2)/rule_size-1),point_1[1]]
		point_4 = [random.randint(0,len(individuo2)/rule_size-1),point_2[1]]
	#print [point_1,point_2]
	#print [point_3,point_4]
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
	print "P: " + str(P)
	fitness_list = compute_fitness(P, ejemplos)
	print "fitness: " + str(fitness_list)	
	iter = 0
	while( iter < 100):
		n = int(round((1-r)*p))
		PS = weel_select(P, n, get_total_fit(fitness_list), fitness_list)
		#print "PS weel: "+ str(PS)
		n = p - n
		parents = tournament_select(P, n, get_total_fit(fitness_list), fitness_list)
		#print "Parents tournament: " + str(parents)
		offspring = crossover_population(parents)
		#print "New offspring: " + str(offspring)
		PS = PS + offspring
		#print "PS: "+str(PS)
		mutate_population(PS,m)
		#print "PS after mutation: " + str(PS)
		PS = add_altern(PS)
		#print "add_altern con 0.01" + str(PS)
		PS = drop_cond(PS)
		#print "drop_cond con 0.6" + str(PS)
		P = PS
		print "P: " + str(P)
		fitness_list = compute_fitness(P, ejemplos)
		print "fitness: " + str(fitness_list)
		iter += 1

		
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
	global rule_size, mask_atributos
	# luego hay que cambiarlos para los ejemplos dados

	population = read_population(opts.file_name)
	#data debe crearse con un vector de numero de intervalos... cada uno representaria el numero de divisiones del elemento i del rasgo continuo
	data = create_data(population,[1000,1000,1000,1000,1000,10000])
	ejemplos = encode_population(population,data)
	rule_size = len(ejemplos[0])
	mask_atributos = ['11000', '00110']

	back_population = decode_population(ejemplos,data)
	GA(ejemplos, opts.p, opts.r, opts.m)
	
	


if __name__ == "__main__":
    main()

	
