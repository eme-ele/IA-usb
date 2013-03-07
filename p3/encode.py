import random

# En esta funcion entra el numero binario sin el antecedente "0b" que llevan normalmente los resultantes de la funcion bin()
def complete_bin(size,binario):
	original_size = len(binario)
	if original_size == size:
		return binario
	for x in range(size - original_size) :
		binario = '0' + binario
	return binario




def continue_clasification(lim_inf, lim_sup, div, value):
	size = len(bin(div)[2:])
	step = (lim_sup - lim_inf)/float(div)
	#print div
	for x in range(1,2**size):
		if value < lim_inf + step*x:
			return complete_bin(size,bin(x-1)[2:])

def continue_reversion(lim_inf, lim_sup, div, value):
	part = int(value,2)
	step = (lim_sup - lim_inf)/float(div)
	return round(lim_inf + step*part,2)



def bin_to_list(binary,datos):
	lista = []
	elem = ""
	for x in range(16):
		if dictionary[x]:
			#print "dic in A" + str(x+1)
			elem = binary[:len(dictionary[x].items()[0][1])]
			binary = binary[len(dictionary[x].items()[0][1]):]
		else:
			#print "con in          A" + str(x+1)
			elem = binary[:len(bin(datos[x][2])[2:])]
			binary = binary[len(bin(datos[x][2])[2:]):]
		lista.append(elem)
	return lista


def mask_matrix(bin_rule,datos):
	lista = bin_to_list(bin_rule,datos)
	matrix = []
	for x in range(16):
		new = ""
		for y in range(16):
			if x==y:
				new += '1'*len(lista[y])
			else:
				new += '0'*len(lista[y])
		matrix.append(new)
	return matrix

#DICCIONARIO DE TERMINOS

A1 = dict({"b" : "0", "a" : "1"})
A4 = dict({"u":"00", "y":"01", "l":"10", "t":"11"})
A5 = dict({"g":"00", "p":"01", "gg":"10"})
A6 = dict({"c":"0000", "d":"0001", "cc":"0010", "i":"0011", "j":"0100", "k":"0101", "m":"0110", "r":"0111", "q":"1000", "w":"1001", "x":"1010", "e":"1011", "aa":"1100", "ff":"1101"})
A7 = dict({"v":"0000", "h":"0001", "bb":"0010", "j":"0011", "n":"0100", "z":"0101", "dd":"0110", "ff":"0111", "o":"1000"})
A9 = dict({"t":"0", "f":"1"})
A10 = dict({"t":"0", "f":"1"})
A12 = dict({"t":"0", "f":"1"})
A13 = dict({"g":"00", "p":"01", "s":"10"})
A16 = dict({"-":"0", "+":"1"})
dictionary = [A1,0,0,A4,A5,A6,A7,0,A9,A10,0,A12,A13,0,0,A16]


def encode(features, data):
	if len(features)!=16:
		print "dimension de arreglo incorrecto"
		exit(-1)
	binary = ""
	for x in range(16):
		if data[x]:
			binary =binary + continue_clasification(data[x][0],data[x][1],data[x][2],features[x])
		elif dictionary[x]:
			binary = binary + dictionary[x][features[x]]
		else:
			print "mala correspondencia entre data y dictionary"
			exit(-1)
	return binary


def decode(features,data):
	lista = []
	for x in range(16):
		if dictionary[x]:
			for key,value in dictionary[x].items():
				if value == features[x]:
					lista.append(key)
					break
		else:
			lista.append(continue_reversion(data[x][0],data[x][1],data[x][2],features[x]))
	return lista

def random_binary(tam):
	res = ""
	for x in range(tam):
		if random.random() >= 0.5:
			res = res + "1"
		else:
			res = res + "0"
	return res


def mutation(individuo):
	point = random.randint(0,len(individuo)-1)
	return individuo[:point] + str(int(not int(individuo[point]))) + individuo[point+1:]
	


def mutate_population(PS,r):
	number = round(PS*r)
	PS_shuffle = random.shuffle(PS)
	
	for individuo in range(number):
		PS_shuffle[individuo] = mutation(PS_shuffle[individuo])
	return PS_shuffle

def test():
	ejemplo = ['b',41.92,0.42,'u','g','c','h',0.21,'t','t',6,'f','g',220,948,'+']
	datos = [0,[30,60,3000],[0,1,1000],0,0,0,0,[0,1,1000],0,0,[0,10,2000],0,0,[200,300,1000],[900,1000,10000],0]
	print ejemplo
	binary = encode(ejemplo,datos)
	binary = random_binary(len(binary))
	print binary
	print len(binary)
	features = bin_to_list(binary,datos)
	print features
	print decode(features,datos)
	print mutation("000111000111000111")
	m = mask_matrix(binary,datos)
	for x in m:
		print x

def rueda_ruleta(probabilities):
	prob.sort(reverse=True)
	lanzamiento = random.random()
	circle = 0
	for elem in range(prob):
		circle+=prom[elem]
		if lanzamiento <= circle:
			return elem 



'''def crossover(individuo1,individuo2,rule_size):
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
	print [point_1,point_2]
	print [point_3,point_4]
	son1 = individuo1[:point_1[0]*rule_size+point_1[1]] + individuo2[point_3[0]*rule_size+point_3[1]:point_4[0]*rule_size+point_4[1]] + individuo1[point_2[0]*rule_size+point_2[1]:] 
	son2 = individuo2[:point_3[0]*rule_size+point_3[1]] + individuo1[point_1[0]*rule_size+point_1[1]:point_2[0]*rule_size+point_2[1]] + individuo2[point_4[0]*rule_size+point_4[1]:] 
	return [son1,son2]'''
	


if __name__ == '__main__':



	test()
	#x,y = crossover('111111111111111111111111111111111111111111111111', '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',48)
	#print x
	#print y
	





