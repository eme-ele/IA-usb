import sys
import re
from nltk import SnowballStemmer


'''
CARACTERISTICAS POLARES
numero de palabras positivas y negativas
numero de emoticons positivos y negativos 
numero de palabras con all-cap
numero de palabras enfatizadas (repeticiones de letras)
numero de grupos de signos de exclamacion  
porcentaje del texto capitalizado


OTRAS CARACTERISTICAS
numero de palabras en el tweet
numero de hashtags
numero de URLs
numero de signos de puntuacion
'''
stemmer = SnowballStemmer("spanish")
def numero_palabras_positivas(tweet):
	res = 0
	twt = tweet.split()
	try:
		stemmer = SnowballStemmer("spanish")
		for w in twt:
			if stemmer.stem(unicode(w.strip(),'UTF-8')).encode("UTF-8") in positivas_list:
				res += 1
	except:
		pass
	return res
	
def numero_palabras_negativas(tweet):
	res = 0
	twt = tweet.split()
	try:
		for w in twt:
			if stemmer.stem(unicode(w.strip(),'UTF-8')).encode("UTF-8") in negativas_list:
				res += 1
	except:
		pass
	return res

def numero_emoticons_positivos(tweet):
	res = 0
	twt = tweet.split()
	for w in twt:
		for p in pos_emoticons_list:
			if w == p:
				res += 1
	return 0

def numero_emoticons_negativos(tweet):
	res = 0
	twt = tweet.split()
	for w in twt:
		for p in neg_emoticons_list:
			if w == p:
				res += 1
	return 0

def numero_palabras_allCAP(tweet):
	all_cap_form = re.compile(r'\b[A-Z]+\b')
	return len(re.findall(all_cap_form,tweet))

def numero_enfazis(tweet):
	repetition_form = re.compile(r'([A-Za-z])\1')
	return len(re.findall(repetition_form,tweet))

def numero_exclamacion(tweet):
	exclamacion_form = re.compile(r'!+')
	return len(re.findall(exclamacion_form,tweet))


def proporcion_capitalizada(tweet):
	cap_form = re.compile(r'[A-Z]')
	return float(len(re.findall(cap_form,tweet)))/float(len(tweet))


def numero_palabras(tweet):
	return len(tweet.split(' '))

def numero_hashtags(tweet):
	hashtags_form = re.compile(r'#[A-Za-z0-9_]+')
	return len(re.findall(hashtags_form,tweet))

######### FALTA REGEX ####################
def numero_urls(tweet):
	url_form = re.compile(r'http\S+\tU\n')
	return len(re.findall(url_form,tweet))

def numero_puntuaciones(tweet):
	puntuacion_form = re.compile(r'[^A-Za-z0-9\s]+')
	return len(re.findall(puntuacion_form,tweet))


def feature_list(tweet):
	return [numero_palabras_positivas(tweet),	numero_palabras_negativas(tweet),	numero_emoticons_positivos(tweet),	numero_emoticons_negativos(tweet),	numero_palabras_allCAP(tweet),	numero_enfazis(tweet),	numero_exclamacion(tweet),	proporcion_capitalizada(tweet),		numero_palabras(tweet),		numero_hashtags(tweet),		numero_urls(tweet),		numero_puntuaciones(tweet)]

def read_lista_palabras(origen):
	lista = []
	f = open(origen)
	for l in f:
		lista.append(l.strip())
	return set(lista)
	

def read_archivo(origen, destino):
	f = open(origen)
	g = open(destino,'w')
	for line in f:
		clase = line[0]
		if clase == "N":
			clase = '0'
		elif clase == "O":
			clase = '1'
		elif clase == "P":
			clase = '2'
		else:
			print "ERROR class ==" + clase
			exit(-1)
		features = feature_list(line[2:])
		g.write(clase)
		g.write(" ")
		for feat in features:
			g.write(str(feat))
			g.write(" ")
		g.write("\n")
	g.close()
	f.close()

if __name__ == "__main__":
	positivas_list = read_lista_palabras("data/stemm_positivas.data")
	negativas_list = read_lista_palabras("data/stemm_negativas.data")
	pos_emoticons_list = read_lista_palabras("data/emot_positivos.data")
	neg_emoticons_list = read_lista_palabras("data/emot_negativos.data")
	read_archivo(sys.argv[1],sys.argv[2])



