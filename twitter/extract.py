import tweepy
import sqlite3
import optparse
import time

def create_tables():
	# telefonias
	try:
		cur.execute("CREATE TABLE digitel (date text, user text, user_id int, tweet_id int, text text)")
		cur.execute("CREATE TABLE movistar (date text, user text, user_id int, tweet_id int, text text)")
		cur.execute("CREATE TABLE movilnet (date text, user text, user_id int, tweet_id int, text text)")
	except:
		return
	# tweets generales 
	#cur.execute("CREATE TABLE random (date text, user text, user_id int, tweet_id int, text text)")
	# basados en emoticones
	#cur.execute("CREATE TABLE positive (date text, user text, user_id int, tweet_id int, text text)")
	#cur.execute("CREATE TABLE negative (date text, user text, user_id int, tweet_id int, text text)")


def insert_tweet(tweet, table_name): 
	date = tweet.created_at
	user = tweet.from_user
	user_id = tweet.from_user_id_str
	tweet_id = tweet.id_str
	text = tweet.text.encode('utf-8')
	with con: 
		try:
			query = "INSERT INTO "+ table_name + " VALUES(?, ?, ?, ?, ?, ?)"
			cur.execute(query, (date, user, user_id, tweet_id, text))
		except:
			return


def extract(query, table_name):
	lat = 6.42375
	lon = -66.58973
	rad = '1mi'
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
				maxid = tweet.id_str()
				prev_maxid = maxid
			else:
				# all done
				break
    		page += 1  # next page

		page = 1


def create_dataset():
	extract("digitel", "digitel")
	extract("movistar", "movistar")
	extract("movilnet", "movilnet")


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

