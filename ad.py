import tracery
from tracery.modifiers import base_english
from textblob import TextBlob, Word
import sys
import random
import markov
import json

ads_file = open('ads.json').read()
ads_data = json.loads(ads_file)


rules = {
    'start': ads_data['start'],
    'middle': ads_data['middle'],
    'end': ads_data['end'],
    'ad': ["#start# #middle# #middle# #middle# #end#"]
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
content = grammar.flatten("#ad#") 


#pick a sponsor name by mashing up the first part of a random noun from corpora and the second half of a real company name
def halfsies(left, right):
  left_part = left[:len(left)/2]
  right_part = right[len(right)/2:]
  return left_part + right_part


sponsor_names = ("Squarespace", "Casper", "Mail chimp", "Loot Crate", "Audible.com", "Nature Box", "Harry's", "Seeso", "KIND Snacks", "Slack", "Sabra Hummus")
nouns_file = open('nouns.json').read()
nouns_data = json.loads(nouns_file)

nouns_list = nouns_data['nouns']


sponsor = halfsies(random.choice(nouns_list).title(), random.choice(sponsor_names))
print "Sponsor: " + sponsor

content_str = str(content)

output = list()
nouns = list()

for item in content_str.split():
	item = item.replace("*Sponsor*", sponsor)
	item = item.replace("_code_", "BeepBoop")
	output.append(item)
print " ".join(output)








# print content_str

# blob = TextBlob(content_str)

# for word, tag in blob.tags: 
# 	if tag.startswith('NN'):
# 		if len(word) > 4 and len(word.synsets) > 0:
# 			synset = random.choice(word.synsets)
# 			lemma = random.choice(synset.lemma_names())
# 			output.append(lemma.replace("_", " "))
# 		else:
# 			output.append(word)

# print " ".join(output)



# for item in content_str.split():
# 	item = item.strip()
# 	item = item.replace("*Sponsor*", sponsor)
# 	item = item.replace("_code_", "BeepBoop")
# 	print "".join(item)



