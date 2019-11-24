import nltk
from nltk.corpus import stopwords
import re
from textblob import TextBlob
import string
import datetime

class Tweet:

	# regex borrowed from https://gist.github.com/gruber/8891611
	url_regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

	#HappyEmoticons
	emoticons_happy = set([
		':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',	
		':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',	
		'=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',		
		'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',		
		'<3'])

	# Sad Emoticons
	emoticons_sad = set([
		
':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
		
':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
		
':c', ':{', '>:\\', ';('
		
])

	emoticons = emoticons_happy.union(emoticons_sad)

	#Emoji patterns
	emoji_pattern = re.compile("["
		
	
 u"\U0001F600-\U0001F64F"  # emoticons
		
	
 u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		
	
 u"\U0001F680-\U0001F6FF"  # transport & map symbols
		
	
 u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		
	
 u"\U00002702-\U000027B0"
		
	
 u"\U000024C2-\U0001F251"
		
	
 "]+", flags=re.UNICODE)

	topics = ["environment", "foreign relations", "national security", "environment", "republicans",
				"healthcare", "guns", "abortion", "civil rights", "connection", "economy", "other"] 
				# connection is trying to show a connection to a voter or other figure


	def __init__(self, raw_text, date, tweeter):
		self.raw_text = raw_text
		self.media = False
		self.outside_link = False
		self.response = False
		self.set_clean_text()
		self.set_sentiment()
		self.date = date
		self.tweeter = tweeter


	def __eq__(self, other):
		return self.raw_text == other.raw_text


	def __ne__(self, other):
		return not self.__eq__(other)


	def __str__(self):
		return self.raw_text

	def __hash__(self):
		return self.raw_text.__hash__()


	def getraw_text(self):
		return self.raw_text


	def set_clean_text(self):
		raw = self.raw_text
		stop_words = set(stopwords.words('english'))
		raw = re.sub(self.url_regex, '', raw)
		
		#after tweepy preprocessing the colon symbol left remain after removing mentions
				
		raw = re.sub(r':', '', raw)
				
		raw = re.sub(r'‚Ä¶', '', raw)
		#replace consecutive non-ASCII characters with a space
				
		raw = re.sub(r'[^\x00-\x7F]+',' ', raw)
				
		#remove emojis from tweet
				
		raw = self.emoji_pattern.sub(r'', raw)
		#filter using NLTK library append it to a string
			
		word_tokens = nltk.word_tokenize(raw)	
		filtered_tweet = [w for w in word_tokens if not w in stop_words]
				
		filtered_tweet = []
		#looping through conditions
		for w in word_tokens:
			#check tokens against stop words , emoticons and punctuations		
			if w not in stop_words and w not in self.emoticons and w not in string.punctuation:
				filtered_tweet.append(w)
				
		self._clean_text = ' '.join(filtered_tweet)
	

	def get_clean_text(self):
		return self._clean_text


	def set_sentiment(self):
		blob = TextBlob(self._clean_text)
		self._sentiment = blob.sentiment     
		self._polarity = blob.sentiment.polarity
		self._subjectivity = blob.sentiment.subjectivity

		
	def get_sentiment(self):
		return self._sentiment


	def get_polarity(self):
		return self._polarity # range from -1 (negative) to 1 (positive)


	def get_subjectivity(self):
		return self._subjectivity # range from 0 (objective) to 1 (subjective)
		
	def contains_media(self):
		self.media = True

	def contains_link(self):
		self.outside_link = True

	def is_response(self):
		self.response = True