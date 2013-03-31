import tweepy
import sqlite3
import optparse
import time


def create_tables():
	with con:
		try:
			#cur.execute("DROP TABLE digitel")
			#cur.execute("DROP TABLE movistar")
			#cur.execute("DROP TABLE movilnet")
			#cur.execute("CREATE TABLE digitel (date text, user text, user_id int, tweet_id int, text text)")
			#cur.execute("CREATE TABLE movistar (date text, user text, user_id int, tweet_id int, text text)")
			#cur.execute("CREATE TABLE movilnet (date text, user text, user_id int, tweet_id int, text text)")
			#cur.execute("CREATE TABLE random (date text, user text, user_id int, tweet_id int, text text)")
			cur.execute("CREATE TABLE positivo (date text, user text, user_id int, tweet_id int, text text)")
			cur.execute("CREATE TABLE negativo (date text, user text, user_id int, tweet_id int, text text)")


		except:
			print "error creando tablas"
			exit(-1);


def insert_tweet(tweet, table_name): 
	print tweet.text.encode('utf-8')
	date = tweet.created_at
	user = tweet.from_user
	user_id = tweet.from_user_id_str
	tweet_id = tweet.id_str
	text = tweet.text
	query = "INSERT INTO "+ table_name + " VALUES(?, ?, ?, ?, ?)"
	with con: 
		try:
			cur.execute(query, (date, user, int(user_id), int(tweet_id), text))
		except sqlite3.Error as e:
			print e
			return
			#print "TWEET NO INGRESADO"
			#exit(-1)


def extract(query, table_name):
	lat = 10.50
	lon = -66.90
	rad = '4mi'
	ven_code = '%s,%s,%s' % (lat, lon, rad)
	page = 1
	prev_maxid = 0
	maxid = 0
	
	while (prev_maxid != maxid or maxid == 0):
	
		while (page < 16):
			try:
				if (maxid == 0):
					retrieved = tweepy.api.search(query, page=page, rpp=100, geocode=ven_code, lang='es')
				else:
					retrieved = tweepy.api.search(query, page=page, rpp=100, geocode=ven_code, lang='es', max_id=maxid)					
			except tweepy.error.TweepError, e:
				string = str(e)
				if string.rstrip() == "You have been rate limited. Enhance your calm.":
					print "Rate limited. Waiting."
					time.sleep(600)
					continue
			if retrieved:
				for tweet in retrieved:
					insert_tweet(tweet, table_name)
				maxid = tweet.id_str
				prev_maxid = maxid
			else:
				# all done
				break
    		page += 1  # next page

		page = 1


def create_dataset():
	extract(":-) OR :) OR =) OR :D OR =D", "positivo")
	extract(":-( OR :( OR =( OR :C", "negativo")
	#extract("digitel", "digitel")
	#extract("movistar", "movistar")
	#extract("movilnet", "movilnet")


def main():
	parser = optparse.OptionParser()
	parser.add_option('-d', help='database name', type='string', dest='db_name')
	(opts, args) = parser.parse_args()
	mandatories = ['db_name']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)

	# conexion con la base de datos
	global con, cur
	con = sqlite3.connect(opts.db_name)
	cur = con.cursor()

	create_tables()
	create_dataset()


	

if __name__ == "__main__":
    main()

