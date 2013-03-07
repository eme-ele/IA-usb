import optparse
import random
import math

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
	pass
	


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
	number = round(PS*r)
	PS_shuffle = random.shuffle(PS)
	
	for individuo in range(number):
		PS_shuffle[individuo] = mutation(PS_shuffle[individuo])
	return PS_shuffle


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
			hipotesis = complete_bin(rule_size, altern_bin[2:])
		drop_PS.append(hipotesis)
	return drop_PS


def GA(ejemplos, p, r, m):
	print "ejemplos: " + str(ejemplos)
	P = poblacion(len(ejemplos[0]), p)
	print "P: " + str(P)
	fitness_list = compute_fitness(P, ejemplos)
	while(1):
		n = int(round((1-r)*p))
		#print "weel_select(" + str(P ) + ", " +  str(n) +", "+ str(get_total_fit(fitness_list)) + ", " + str(fitness_list) + ")"
		PS = weel_select(P, n, get_total_fit(fitness_list), fitness_list)
		print "PS: "+ str(PS)
		n = p - n
		parents = weel_select(P, n, get_total_fit(fitness_list), fitness_list)
		print "To be crossed: " + str(parents)
		offspring = crossover_population(parents)
		print "New offspring: " + str(offspring)
		PS = PS + offspring
		print "PS: "+str(PS)
		PS = add_altern(PS)
		print "add_altern con 0.01" + str(PS)
		PS = drop_cond(PS)
		print "drop_cond con 0.6" + str(PS)
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
	global rule_size, mask_atributos
	# luego hay que cambiarlos para los ejemplos dados
	ejemplos = ['10101', '10011', '01101', '01010']
	rule_size = 5
	mask_atributos = ['11000', '00110']

	GA(ejemplos, opts.p, opts.r, opts.m)
	
	


if __name__ == "__main__":
    main()

	
