import tracery
from tracery.modifiers import base_english
from textblob import TextBlob, Word
import urllib
import random
import markov
import json
import wikipedia

url = "http://api.wordnik.com:80/v4/word.json/bot/examples?includeDuplicates=false&useCanonical=false&skip=0&limit=5&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"

content = {
    'definition': ["HOST: So what is a bot? \n\nGUEST: Well, a bot is #defs#, sometimes also described as #defs#. Another way to say it: #examples#"]
}

defs_list = list()

for line in open('defs.txt').readlines():
	line = line.decode('utf8')
	line = line.strip()
	line = line.lower()
	defs_list.append(line)

content.update({'defs': defs_list})

# wiki = wikipedia.page("chatterbot")
# blob = TextBlob(wiki.summary)
# #print blob.sentences

# print type(blob.noun_phrases)


# questions = list()
# blob = TextBlob(open('tal.txt').read().decode('utf8'))
# for question in blob.sentences:
# 	question = question.replace("\n", " ")
# 	if "?" in question and "Ira" in question:
# 		question = question.replace("Ira Glass", "Host: ")
# 		print question


def getHostQuestions(transcript, hostNameShort, hostNameLong):
	questions = list()
	blob = TextBlob(open(transcript).read().decode('utf8'))
	for question in blob.sentences:
		question = question.replace("\n", " ")
		if "?" in question and hostNameShort in question:
			question = question.replace(hostNameLong, "Host: ")
			questions.append(question)
	return questions

#print getHostQuestions('tal.txt', 'Ira', 'Ira Glass')
#print getHostQuestions('replyall.txt', 'PJ', 'PJ VOGT')
RA = getHostQuestions('replyall.txt', 'Alex', 'ALEX GOLDMAN')


raw_data = urllib.urlopen(url).read().decode('utf8')
data = json.loads(raw_data)

exs_list = list()

for item in data['examples']:
	exs_list.append(item['text'])

content.update({'examples': exs_list})



# print blob.sentences



grammar = tracery.Grammar(content)
grammar.add_modifiers(base_english)
interview = grammar.flatten("#definition#") 
print interview

