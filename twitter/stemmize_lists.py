import optparse
from nltk import SnowballStemmer


def main():
	parser = optparse.OptionParser()
	parser.add_option('-f', help='archivo de la lista', type='string', dest='in_file')
	parser.add_option('-o', help='archivo de salida', type='string', dest='out_file')
	(opts, args) = parser.parse_args()
	mandatories = ['in_file', 'out_file']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)

	lista = open(opts.in_file, 'r')
	output = open(opts.out_file, 'w')

	stemmer = SnowballStemmer("spanish")

	for word in lista:
		output.write(stemmer.stem(unicode(word.strip(),'UTF-8')).encode("UTF-8")+"\n")

	lista.close()
	output.close()


if __name__ == "__main__":
    main()

