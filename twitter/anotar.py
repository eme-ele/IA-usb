import optparse


def main():

	parser = optparse.OptionParser()
	parser.add_option('-f', help='archivo de datos', type='string', dest='in_file')
	parser.add_option('-o', help='archivo de salida', type='string', dest='out_file')
	(opts, args) = parser.parse_args()
	mandatories = ['in_file', 'out_file']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)

	tweets = open(opts.in_file, 'r')
	output = open(opts.out_file, 'w')

	for i in range(150):
		line = tweets.readline()
		print "\n"+line
		tag = raw_input("Positivo (P), Negativo (N) o Neutro (O): ")
		output.write(tag+"\t"+line)

	output.close()
	tweets.close()
		


if __name__ == "__main__":
    main()

