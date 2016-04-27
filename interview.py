
from textblob import TextBlob, Word
import urllib
import random
import markov
import json
import wikipedia


topic = "bot"

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
	guest_full_name = " ".join([honorific, first_name, last_name]) + ", " + " ".join([topic, occupation])
	return honorific, first_name, last_name, occupation, guest_full_name


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
		if item.sentiment.polarity > 0:
			positive.append(item)
		else:
			negative.append(item)
	return positive, negative

all_examples = doJSON(url, 'examples', 'text', 'y', 'y')
all_first_names = doJSON('first_names.json', "firstNames", '', 'n', 'n')
all_last_names = doJSON('last_names.json', "lastNames", '', 'n', 'n')
all_occupations = doJSON('occupations.json', "occupations", '', 'n', 'n')
all_honorifics = doJSON('honorifics.json', "englishHonorifics", '', 'n', 'n')

g_honorific, g_first_name, g_last_name, g_occupation, g_full_name = guestGenerator()


def hostGenerator():
	host_first_names = ['Ira', 'Sarah', 'PJ', 'Alex', 'Alex', 'Anna', 'Jad', 'Dan', 'Robert', 'Starlee', 'Joe', 'Mike', 'Marc', 'Roman', 'Heben', 'Tracy', 'Brittany', 'Ed', 'Peter']
	host_last_names = ['Glass', 'Koenig', 'Vogt', 'Blumberg', 'Goldman', 'Sale', 'Abumrad', 'Savage', 'Krulwich', 'Kine', 'Rogan', 'Rowe', 'Mars', 'Nigatu', 'Clayton', 'Luse', 'Levine', "Sagal"]

	first_name = halfsies(''.join(random.sample(host_first_names, 1)), ''.join(random.sample(host_first_names, 1)))
	last_name = halfsies(''.join(random.sample(host_last_names, 1)), ''.join(random.sample(host_last_names, 1)))

	host_full_name = first_name + " " + last_name
	return first_name, last_name, host_full_name

h_first_name, h_last_name, h_full_name = hostGenerator()


defs_list = list()

for line in open('defs.txt').readlines():
	line = line.decode('utf8')
	line = line.strip()
	line = line.lower()
	defs_list.append(line)


wiki = wikipedia.page("chatterbot")
wikiblob = TextBlob(wiki.summary)
nps = wikiblob.noun_phrases



tal = getHostQuestions('tal.txt', 'Ira', 'Ira Glass')
RA_Alex = getHostQuestions('replyall.txt', 'ALEX', 'ALEX: ')
RA_PJ = getHostQuestions('replyall.txt', 'PJ', 'PJ: ')
RL_Jad = getHostQuestions('radiolab.txt', 'JAD ABUMRAD', 'JAD ABUMRAD: ')
RL_Robert = getHostQuestions('radiolab.txt', 'ROBERT KRULWICH', 'ROBERT KRULWICH: ')

all_questions = tal + RA_PJ + RA_Alex + RL_Jad + RL_Robert




all_adjs = open('adjectives.txt').read()
adj_blob = TextBlob(all_adjs)


pos_adjs, neg_adjs = getSentiment(adj_blob.sentences)


pos_host_questions_list, neg_host_questions_list = getSentiment(all_questions)



answers_inc_bot_list = list()
answers_other_list = list()
all_article_questions = list()
article_questions_inc_bot = list()


articles = open('articles.txt')
blob = TextBlob(articles.read().decode('utf8'))
for answer in blob.sentences:
	answer = answer.replace("\n", " ")
	if "bot" in answer:
		answers_inc_bot_list.append(answer)
	else:
		answers_other_list.append(answer)
	if "?" in answer:
		if "bot" in answer:
			article_questions_inc_bot.append(answer)
		else:
			all_article_questions.append(answer)

all_text = answers_inc_bot_list + answers_other_list + all_questions




markov_a = ' '.join(markov.word_level_generate(all_text, 3, count=4))


print "HOST: Welcome to Beep Boop, a computer generated podcast. I'm your host, " + h_full_name + "."
print "Every week we will bring in a guest to discuss one " + getRandom(pos_adjs, 'y').replace(".", "") + ", " + getRandom(pos_adjs, 'y').replace(".", "") + " topic that everyone is talking about on the internet. We hope that you will find it " + getRandom(pos_adjs, 'y')
print "This week is episode 1, where we will be covering the " + getRandom(pos_adjs, 'y').replace(".", "") + " but " + getRandom(neg_adjs, 'y').replace(".", "") + " world of " + Word(topic).pluralize() + "."
print "I'm happy" + " to announce that our guest this week is " + g_full_name + ". Very excited to have you here.\n"
print "GUEST: Thank you, I'm glad to be here, " + h_first_name + ". \n"
print "HOST: So what is a " + topic + "? \n"
print "GUEST: Well, a " + topic + " is " + random.choice(defs_list) + ", sometimes also described as " + random.choice(defs_list) + ", or a " + getRandom(nps, 'n') + ". Another way to say it: " + getRandom(all_examples, 'n') + "\n"
print "HOST: Let me ask you, " + str(g_first_name) + ", " + getRandom(article_questions_inc_bot, 'y') + "\n"
print "GUEST: " + getRandom(answers_inc_bot_list, 'y') + " " + getRandom(answers_other_list, 'y') + "\n"
print "HOST: I've heard that " + getRandom(all_examples, 'n') + "\n"
print "GUEST: " + markov_a + '\n'
print "HOST: Fascinating." + '\n'
print "GUEST: Some find it " + getRandom(neg_adjs, 'y')




