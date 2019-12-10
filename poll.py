import datetime
from candidate import *

class Poll:

	def __init__(self, poll):

		poll_date = poll["Date"].split(" - ")
		poll_start_date = poll_date[0].split("/")
		poll_end_date = poll_date[1].split("/")
		self.start_date = datetime.date(2019, int(poll_start_date[0]), int(poll_start_date[1]))
		self.end_date = datetime.date(2019, int(poll_end_date[0]), int(poll_end_date[1]))
		self.name = poll["Poll"]
		self.poll_data = poll

		#returns tuple of (percentage, candidate name), sorted by a candidate's position in the polls, 1st to last
		self.sorted_results = self.sort_results(poll)


	def __eq__(self, other):
		return (self.name == other.name and self.end_date == other.end_date)


	def __ne__(self, other):
		return not self.__eq__(other)


	def __str__(self):
		return (self.name + " (" + str(self.end_date) + ")") 


	def __hash__(self):
		return self.name.__hash__()

	def __gt__(self, poll2):
		return self.end_date > poll2.end_date


	def get_sorted_results(self):
		return self.sorted_results


	def sort_results(self, poll):  # fix this
		results = [] #list of tuples that have (candidate's percentage, candidate's name)
		for person in poll:
			if person != "Poll" and person != "Date" and person != "Spread":
				if person != "Bloomberg" and person != "Steyer" and poll[person] != '--':
					results.append((float(poll[person]), person))
		results.sort(key = lambda x:x[0])
		return results


	def update_candidates(self, candidate_set):
		for i in range(len(self.sorted_results)):
			person = self.sorted_results[i]
			if person[1] not in candidate_set:
				cand = Candidate(person[1])
				candidate_set.add(cand)
			for c in candidate_set:
				if c == person[1]:
					c.add_poll(self, len(self.sorted_results)-i, person[0])
					break
		return candidate_set
