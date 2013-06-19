import json
import sys
import operator
from numpy import mean

# scores returns a dictionary with the sentiment scores
def get_scores(fn):
	afinnfile = open(fn)
	scores = {}
	for line in afinnfile:
		term, score  = line.split("\t")
		scores[term] = int(score)

	return scores

# extract the text from tweets given by a live twitter stream
# provided that the country code is that of the US
def tweet_text(fn):
	tweet_file = open(fn)
	tweets = []
	for line in tweet_file:
		dict_line = json.loads(line)
		if ('text' in dict_line and 'place' in dict_line):
				if ( dict_line['place'] is not None):
					if (dict_line['place']['country_code']=='US' and dict_line['place']['full_name'] is not None):
						tweets.append({'text': dict_line['text'].encode('utf-8'),'state':dict_line['place']['full_name'][-2:]})

	return tweets

#keep track of the words which have to be removed
def word_remove(word):
	remove_start = ('@', 'http')
	if word.startswith(remove_start):
		return True

# compute the sentiment score of a text by adding up the sentiment scores of the words in the text
# eliminate the characters rem_char from the text
# have decided to include hashtags of tweets
def sentiment_score(text,scores):
	score = 0
	rem_chars = "&(){}<>:.,''#"
	text = ''.join(c for c in text if c not in rem_chars)
	
	words = text.split(' ')	
	words[:] = [word.lower() for word in words if not word_remove(word)]

	for word in words:
		if word in scores:
			score = score + scores[word]

	return score

# get the state abbreviations
def get_state_abbr():
	abbr_file = open('states.csv')
	states ={}

	for line in abbr_file:
		line = ''.join(c for c in line if c is not '"').replace('\n','')
		line_list = line.split(',')
		if(len(line_list[1])==2):
			states[line_list[1]] = line_list[0].lower()

	return states

#compute the score per state
def sent_state(tweets):
	state_names = get_state_abbr()

	state_scores = {}
	for state in state_names:
		state_scores[state_names[state]] = []
	
	# double-check whether the state of the tweet is an actual state
	for tweet in tweets:
		if (tweet['state'] in state_names):
			if(tweet['score']!=0):
				state_scores[state_names[tweet['state']]].append(tweet['score'])

	for state in state_names:
		state_scores[state_names[state]] = list_av(state_scores[state_names[state]])

	#to scale back the sentiment scores between -1 and +1
	max_score = max( max(state_scores.iteritems(), key=operator.itemgetter(1))[1], 
							-min(state_scores.iteritems(), key=operator.itemgetter(1))[1])

	f = open('sent_scores', 'w')
	f.write("state,sentiment\n")
	if (max_score>0):
		for state in state_names:
				f.write(state_names[state]+","+str(state_scores[state_names[state]]/max_score)+"\n")
	else:
		for state in state_names:
			f.write(state_names[state]+","+str(state_scores[state_names[state]])+"\n")

	f.close()


def list_av(l):
	if (len(l)==0):
		return 0.0
	else:
		return mean(l)

def main():
	sent_file = sys.argv[1]
	tweet_file = sys.argv[2]
	scores = get_scores(sent_file)
	tweets = tweet_text(tweet_file)
	for tweet in tweets:
		tweet['score'] = sentiment_score(tweet['text'],scores)
	sent_state(tweets)

if __name__ == '__main__':
	main()