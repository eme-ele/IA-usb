import random
from gabil import *

# En esta funcion entra el numero binario sin el antecedente "0b" que llevan normalmente los resultantes de la funcion bin()
def complete_bin(size,binario):
	original_size = len(binario)
	if original_size == size:
		return binario
	for x in range(size - original_size) :
		binario = '0' + binario
	return binario




def continue_clasification(lim_inf, lim_sup, div, value):
	size = len(bin(div)[1:])
	step = (lim_sup - lim_inf)/float(div)
	#print div
	if value == "?":
		return "1"*size
	for x in range(1,2**size):
		#print "value: " + str(value) + "< limite inferior + step*x" + str(lim_inf + step*x)
		
		next = lim_inf+step*x
		if float(value) < float(next):
			return complete_bin(size,bin(x-1)[2:])

def continue_reversion(lim_inf, lim_sup, div, value):
	print " " + str(value)
	if value[0] == "1":
		return "?"
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
			elem = binary[:len(bin(datos[x][2])[1:])]
			binary = binary[len(bin(datos[x][2])[1:]):]
		lista.append(elem)
	lista.append(binary)
	
	return lista


def mask_matrix(bin_rule,datos):
	lista = bin_to_list(bin_rule,datos)
	#print len(bin_rule)
	c = 0
	for l in lista:
		c += len(l)
	#print c
	#print c
	matrix = []
	for x in range(16):
		new = ""
		for y in range(16):
			if x==y:
				new += '1'*len(lista[y])
			else:
				new += '0'*len(lista[y])
		matrix.append(new)
	#print len(matrix[0])
	exit(-1)
	return matrix

#DICCIONARIO DE TERMINOS

A1 = dict({"b" : "00", "a" : "01", "?" : "10"})
A4 = dict({"u":"000", "y":"001", "l":"010", "t":"011", "?" : "001"})
A5 = dict({"g":"00", "p":"01", "gg":"10", "?" : "11"})
A6 = dict({"c":"0000", "d":"0001", "cc":"0010", "i":"0011", "j":"0100", "k":"0101", "m":"0110", "r":"0111", "q":"1000", "w":"1001", "x":"1010", "e":"1011", "aa":"1100", "ff":"1101", "?" : "1110"})
A7 = dict({"v":"0000", "h":"0001", "bb":"0010", "j":"0011", "n":"0100", "z":"0101", "dd":"0110", "ff":"0111", "o":"1000", "?" : "1001"})
A9 = dict({"t":"00", "f":"01", "?" : "10"})
A10 = dict({"t":"00", "f":"01", "?" : "10"})
A12 = dict({"t":"00", "f":"01", "?" : "10"})
A13 = dict({"g":"00", "p":"01", "s":"10", "?" : "11"})
A16 = dict({"-":"00", "+":"01", "?" : "10"})
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

def encode_population(population,data):
	bin_pop = []
	for p in population:
		bin_pop.append(encode(p,data))
	return bin_pop



def decode(features,data):
	lista = []
	features =  bin_to_list(features,data)
	for x in range(16):
		if dictionary[x]:
			for key,value in dictionary[x].items():
				if value == features[x]:
					
					lista.append(key)
					break
		else:
			lista.append(continue_reversion(data[x][0],data[x][1],data[x][2],features[x]))
	return lista

def decode_population(population,data):
	feat_pop = []
	for p in population:
		feat_pop.append(decode(p,data))
	return feat_pop


def random_binary(tam):
	res = ""
	for x in range(tam):
		if random.random() >= 0.5:
			res = res + "1"
		else:
			res = res + "0"
	return res


def test():
	ejemplo = ['b',41.92,0.42,'u','g','c','h',0.21,'t','t',6,'f','g',220,948,'+']
	datos = [0,[30,60,3000],[0,1,1000],0,0,0,0,[0,1,1000],0,0,[0,10,2000],0,0,[200,300,1000],[900,1000,10000],0]
	print ejemplo
	binary = encode(ejemplo,datos)
	#binary = random_binary(len(binary))
	print binary
	print len(binary)
	
	features = bin_to_list(binary,datos)
	print features
	print decode(binary,datos)
	print mutation("000111000111000111")
	print  mask_matrix(binary,datos)
	print "hola\n\n\n\n\n\n\n"
	for x in m:
		print x
		print "hola"



if __name__ == '__main__':
	test()
	