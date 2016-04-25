"""
the different parts:

- intro to podcast
- intro of subject and guest
- interview
- ad
- credits

"""

from textblob import TextBlob
import sys
import random
import tracery
from tracery.modifiers import base_english

rules = {
    'origin': '#hello.capitalize#, #location#!',
    'hello': ['hello', 'greetings', 'howdy', 'hey'],
    'location': ['world', 'solar system', 'galaxy', 'universe']
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
print grammar.flatten("#origin#") # prints, e.g., "Hello, world!"
