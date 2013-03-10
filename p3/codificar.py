import random 


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
len_feat = [2,5,5,3,2,4,4,5,2,2,5,2,2,5,5,2]
datos = [0,[13.75,80.25],[0,28],0,0,0,0,[0,28.5],0,0,[0,67],0,0,[0,2000],[0,100000],0]


def parse_file(filename):
	f = open(filename, 'r')
	data = []
	for line in f:
		if line.strip() != '':
			data.append(encode(line.strip().split(',')))
	return data

def complete_bin(size,binario):
	original_size = len(binario)
	if original_size == size:
		return binario
	for x in range(size - original_size) :
		binario = '0' + binario
	return binario


def classify(lim_inf, lim_sup, value, div=26.0):
	size = 5
	step = (lim_sup-lim_inf)/div
	clase = int((value-lim_inf)/step)
	return complete_bin(size, bin(clase)[2:])
		

def encode(example):
	coding = ""
	for x in range(16):
		if dictionary[x]:
			coding += dictionary[x][example[x]]
		else:
			if example[x] == '?':
				coding += '1'*5
			else:
				coding += classify(datos[x][0], datos[x][1], float(example[x]))	
	return coding

def feat_mask():
	feat_mask = []
	for x in range(15):
		mask = ''
		for y in range(len(len_feat)-1):
			if y==x:
				mask += '1'*len_feat[y]
			else:
				mask += '0'*len_feat[y]
		feat_mask.append(mask+'00')
	return feat_mask
		
	
def test():
	ejemplo = ['b',41.92,0.42,'u','g','c','h',0.21,'t','t',6,'f','g',220,948,'+']
	print ejemplo
	binary = encode(ejemplo)
	#binary = random_binary(len(binary))
	print binary
	print len(binary)
	mascaras = feat_mask()	
	print mascaras
	print len(mascaras[0])


if __name__ == '__main__':
	test()
	
