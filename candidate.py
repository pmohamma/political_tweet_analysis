import bisect
import datetime
from poll import *
from tweet import *

class Candidate:


	def __init__(self, name):
		self.name = name
		self.polls = [] # list of tuples that have (poll object, position in poll, and percentage in poll)
		self.tweets = [] # list of tuples that have the tweet objects


	def __eq__(self, other):
		try:
			ret = self.name == other.name
		except:
			ret = self.name == other
		return ret
		

	def __ne__(self, other):
		return not self.__eq__(other)


	def __str__(self):
		return self.name


	def __hash__(self):
		return self.name.__hash__()


	def add_poll(self, poll, position, percentage):
		"""
		poll: Poll object that contains the name and date of the poll
		position: position in the polls. 1 is leader in the poll
		percentage: estimated percentage of support in the poll
		"""
		self.polls = self.sorted_insert(self.polls, (poll, position, percentage))


	def sorted_insert(self, lst, item):
		index = len(lst)
		# Searching for the position 
		for i in range(len(lst)):
			if lst[i][0].end_date > item[0].end_date: 
				index = i 
				break
		  
		# Inserting item in the list 
		lst = lst[:index] + [item] + lst[index:] 
		return lst

	def add_tweet(self, tweet):
		self.tweets.append(tweet)

	def sort_tweets(self):
		self.tweets.sort(key = lambda x: x.date)