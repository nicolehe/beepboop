
from textblob import TextBlob, Word
import urllib
import random
import markov
import json
# import wikipedia
import sys


episode = sys.argv[1]
topic = sys.argv[2]

url = "http://api.wordnik.com:80/v4/word.json/" + topic + "/examples?includeDuplicates=false&useCanonical=false&skip=0&limit=100&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"


def doJSON(file, key, val, moreVal, is_url):
	if is_url is 'y':
		raw_data = urllib.urlopen(file).read().decode('utf8')
	else:
		raw_data = open(file).read().decode('utf8')
	data = json.loads(raw_data)
	words_list = list()
	if moreVal is 'y':
		for item in data[key]:
			words_list.append(item[val])
		return words_list
	else:
		return data[key]

def halfsies(left, right):
  left_part = left[:len(left)/2]
  right_part = right[len(right)/2:]
  return left_part + right_part


def guestGenerator():
	honorific = random.choice(all_honorifics)
	first_name = random.choice(all_first_names)
	last_name = random.choice(all_last_names)
	occupation = random.choice(all_occupations)
	guest_full_name = first_name + " " + last_name
	guest_title = " ".join([honorific, first_name, last_name]) + ", " + " ".join([topic, occupation])
	return honorific, first_name, last_name, occupation, guest_full_name, guest_title

def nameGenerator():
	first_name = random.choice(all_first_names)
	last_name = random.choice(all_last_names)
	full_name = first_name + " " + last_name
	return full_name


def getRandom(list_name, make_str):
	sample = random.sample(list_name, 1)
	if make_str is 'y':
		for item in sample:
			return str(item)
	else:
		for item in sample:
			return item

def getHostQuestions(transcript, hostNameShort, hostNameLong):
	questions = list()
	blob = TextBlob(open(transcript).read().decode('utf8'))
	for question in blob.sentences:
		question = question.replace("\n", " ")
		if "?" in question and hostNameShort in question:
			question = question.replace(hostNameLong, "")
			questions.append(question)
	return questions

def getSentiment(list_name):
	positive = list()
	negative = list()
	for item in list_name:
		if item.sentiment.polarity >= 0:
			positive.append(item)
		else:
			negative.append(item)
	return positive, negative


def hostGenerator():
	host_first_names = ['Ira', 'Sarah', 'PJ', 'Alex', 'Alex', 'Anna', 'Jad', 'Dan', 'Robert', 'Starlee', 'Joe', 'Mike', 'Marc', 'Roman', 'Tracy', 'Brittany', 'Ed', 'Peter', "Lulu", "Alix", "Terry", "Lisa"]
	host_last_names = ['Glass', 'Koenig', 'Vogt', 'Blumberg', 'Goldman', 'Sale', 'Abumrad', 'Savage', 'Krulwich', 'Kine', 'Rogan', 'Rowe', 'Mars', 'Clayton', 'Luse', 'Levine', "Sagal", "Miller", "Spiegal", "Gross", "Chow"]
	first_name = halfsies(''.join(random.sample(host_first_names, 1)), ''.join(random.sample(host_first_names, 1)))
	last_name = halfsies(''.join(random.sample(host_last_names, 1)), ''.join(random.sample(host_last_names, 1)))
	host_full_name = first_name + " " + last_name
	return first_name, last_name, host_full_name

tal = getHostQuestions('corpus/tal.txt', 'Ira', 'Ira Glass')
RA_Alex = getHostQuestions('corpus/replyall.txt', 'ALEX', 'ALEX: ')
RA_PJ = getHostQuestions('corpus/replyall.txt', 'PJ', 'PJ: ')
RL_Jad = getHostQuestions('corpus/radiolab.txt', 'JAD ABUMRAD', 'JAD ABUMRAD: ')
RL_Robert = getHostQuestions('corpus/radiolab.txt', 'ROBERT KRULWICH', 'ROBERT KRULWICH: ')
all_questions = tal + RA_PJ + RA_Alex + RL_Jad + RL_Robert


answers_inc_topic_list = list()
answers_other_list = list()
all_article_questions = list()
article_questions_inc_topic_list = list()


articles = open('corpus/articles.txt').read()
blob = TextBlob(articles.decode('utf8'))
for answer in blob.sentences:
	answer = answer.replace("\n", " ")
	if topic in answer:
		answers_inc_topic_list.append(answer)
	else:
		answers_other_list.append(answer)
	if "?" in answer:
		if topic in answer:
			article_questions_inc_topic_list.append(answer)
		else:
			all_article_questions.append(answer)

all_text = answers_inc_topic_list + answers_other_list + all_questions


all_examples = doJSON(url, 'examples', 'text', 'y', 'y')
all_first_names = doJSON('corpus/first_names.json', "firstNames", '', 'n', 'n')
all_last_names = doJSON('corpus/last_names.json', "lastNames", '', 'n', 'n')
all_occupations = doJSON('corpus/occupations.json', "occupations", '', 'n', 'n')
all_honorifics = doJSON('corpus/honorifics.json', "englishHonorifics", '', 'n', 'n')


pos_host_questions_list, neg_host_questions_list = getSentiment(all_questions)
#generate guest and host names

g_honorific, g_first_name, g_last_name, g_occupation, g_full_name, g_title = guestGenerator()
h_first_name, h_last_name, h_full_name = hostGenerator()




defs_list = list()

for line in open('corpus/defs.txt').readlines():
	line = line.decode('utf8')
	line = line.strip()
	line = line.lower()
	defs_list.append(line)


# wiki = wikipedia.page("chatterbot")
# wikiblob = TextBlob(wiki.summary)
# nps = wikiblob.noun_phrases


all_adjs = open('corpus/adjectives.txt').read()
adj_blob = TextBlob(all_adjs)


pos_adjs, neg_adjs = getSentiment(adj_blob.sentences)


markov_a = ' '.join(markov.word_level_generate(all_text, 2, count=3))
markov_b = ' '.join(markov.word_level_generate(all_text, 2, count=3))

print "BEEP BOOP EPISODE " + episode + ": " + Word(topic).pluralize().upper()
print "\n--------------- \n"
print h_full_name.upper() + ": Welcome to Beep Boop, a computer generated podcast. I'm your host, " + h_full_name + "."
print "Every week we will bring in a guest to discuss one " + getRandom(pos_adjs, 'y').replace(".", "") + ", " + getRandom(pos_adjs, 'y').replace(".", "") + " topic that everyone is talking about on the internet. We hope that you will find it " + getRandom(pos_adjs, 'y')
print "This week is episode " + episode + ", where we will be covering the " + getRandom(pos_adjs, 'y').replace(".", "") + " but " + getRandom(neg_adjs, 'y').replace(".", "") + " world of " + Word(topic).pluralize() + "."
print "I'm happy to announce that our guest today is " + g_title + ". Very excited to have you here.\n"
print g_full_name.upper() + ": Thank you, I'm glad to be here, " + h_first_name + ". \n"
print h_full_name.upper() + ": So what is a " + topic + "? \n"
print g_full_name.upper() + ": Well, a " + topic + " is " + random.choice(defs_list) + ", sometimes also described as " + random.choice(defs_list) + ", or a " + random.choice(defs_list) + ". Another way to say it: " + getRandom(all_examples, 'n') + "\n"
print h_full_name.upper() + ": Let me ask you, " + str(g_first_name) + ", " + getRandom(article_questions_inc_topic_list, 'y') + "\n"
print g_full_name.upper() + ": " + getRandom(answers_inc_topic_list, 'y').decode('utf8') + " " + getRandom(answers_other_list, 'y').decode('utf8') + "\n"
print h_full_name.upper() + ": I've heard that " + getRandom(all_examples, 'n') + "\n"
print g_full_name.upper() + ": " + markov_a + '\n'
print h_full_name.upper() + ": " + getRandom(pos_host_questions_list, 'y') + '\n'
print g_full_name.upper() + ": " + markov_b + '\n'
print h_full_name.upper() + ": Fascinating." + '\n'
print g_full_name.upper() + ": Some find it " + getRandom(neg_adjs, 'y') + '\n'
print h_full_name.upper() + ": Well thank you " + str(g_first_name) + " for this " + getRandom(pos_adjs, 'y').replace(".", "") + " interview.\n"
print g_full_name.upper() + ": Thanks for having me. \n"


print "\n--------------- \n"

from ad import adGenerator

print h_full_name.upper() + ": " + adGenerator()

print "\n--------------- \n"
print h_full_name.upper() + ": Beep Boop is hosted by me, " + h_full_name + ". We were produced this week by " + nameGenerator() + " and " + nameGenerator() + "."
for i in range(4):
	str = "Our " + random.choice(all_occupations) + " is " + nameGenerator() + ". "
	print str.strip()
print "Special thanks to our " + topic + " " + random.choice(all_occupations) + ", " + nameGenerator() + ". Thanks for listening, and see you next week."


