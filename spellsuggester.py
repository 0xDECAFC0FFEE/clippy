from metaphone import doublemetaphone
from jellyfish import damerau_levenshtein_distance
from dictionary_service_client import get_definitions
import json
from sys import argv
import dbm

# input to program from alfred
if len(argv) == 1:
    exit(0)
incorrectly_spelled_word = str(argv[1]).lower()

# getting all metaphonemes of word
metaphonemes = []
for metaphoneme in doublemetaphone(incorrectly_spelled_word):
    if metaphoneme != "":
        metaphonemes.append(metaphoneme)

# getting the possible correctly spelled words from the file
words = []
database = dbm.open("ipa_to_words", "r")
for metaphoneme in metaphonemes:
    words.extend(database[metaphoneme].decode('utf-8').split(" "))
database.close()

# removing duplicate words (metaphonemes might map to the same word)
words = set(words)

# sorting correctly spelled words by damerau lexical distance
words = [(damerau_levenshtein_distance(word.decode('utf-8'), incorrectly_spelled_word.decode('utf-8')), word) for word in words]
words.sort()
words = [word for (editdistance, word) in words]

# trimming to top 30 entries
words = words[:30]

# getting definitions:
word_definitions = get_definitions(words) if words else []
word_definitions = [(word, definition) for word, definition in word_definitions]

# outputing the definitions in alfred-friendly format
if word_definitions:
    items = [{"title": word, "subtitle": definition, "arg": word} for word, definition in word_definitions]
else:
    items = [{"title": "no similar words found", "subtitle": "", "arg": incorrectly_spelled_word}]
output = {"items": items}
print(json.dumps(output, ensure_ascii=True))
