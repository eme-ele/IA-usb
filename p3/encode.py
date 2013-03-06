





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
	for x in range(1,div):
		if value < lim_inf + step*x:
			return complete_bin(size,bin(x-1)[2:])


#DICCIONARIO DE TERMINOS
def A2():
	pass
def A3():
	pass
def A8():
	pass
def A11():
	pass
def A14():
	pass
def A15():
	pass
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

#lista global
def encode(features):
	if len(features)!=16:
		print "dimension de arreglo incorrecto"
		exit(-1)
	return A1[features[0]] + A1[features[0]]



def encode(rasgos):
	print rasgos
	for r in rasgos[1:]:
		print bin(float(r))

