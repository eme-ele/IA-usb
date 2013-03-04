

#lista global


def encode(example):
	pass

#hipotesis es la lista de rasgos y no el codigo binario, al igual que lista
def fitness(hipotesis):
	positivos = 0
	for ejemplo in lista:
		for i in range(len(ejemplo)):
			correcto = ejemplo[i] == hipotesis[i]
			if !correcto:
				break
		positivo += correcto
	return (float(positivos)/float(len(lista)))**2

def probabilidad(hipotesis,P):
	total_fitness = 0 
	for hj in P:
		total_fitness += fitness(hj,lista)
	return 

def select_rueda_ruleta(P,n):
	

	pass
def GA():
	


	