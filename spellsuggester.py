from metaphone import doublemetaphone
import hashlib 
from jellyfish import damerau_levenshtein_distance
from dictionary_service_client import get_definitions
import sys
import os
import json

def pidprint(message):
    # os.system('say "%s"' % message)
    sys.stderr.write("ss %s: %s\n" % (os.getpid(), message))

line_length = 1633
hash_mod_value = 74004
incorrectly_spelled_word = str("{query}").lower()

def filter_empty_string(strings):
    return[string for string in strings if string != ""]

# getting all metaphonemes of word
metaphonemes = []
for metaphoneme in doublemetaphone(incorrectly_spelled_word):
    if metaphoneme != "":
        metaphonemes.append(metaphoneme)

# getting file indexes for metaphoneme
metaphoneme_file_inedexes = []
for metaphoneme in metaphonemes:
    m = hashlib.md5()
    m.update(str.encode(str(metaphoneme)))
    index = int(m.hexdigest(), 16) % hash_mod_value 
    metaphoneme_file_inedexes.append((index, metaphoneme))

# actually getting the possible correctly spelled words from the file
words = []
with open("ipa_to_words.txt", "r") as readFile:
    for index, metaphoneme in metaphoneme_file_inedexes:
        readFile.seek(line_length*index)
        raw_line = str(readFile.readline()).strip()
        metaphoneme_hash_collisions = filter_empty_string(raw_line.split("|"))
        for possible_metaphoneme in metaphoneme_hash_collisions:
            if possible_metaphoneme.startswith(metaphoneme):
                words += filter_empty_string(possible_metaphoneme.split(" "))[1:]
                break

pidprint("loading words from file")

# removing duplicates
words = list(set(words))

# sorting correctly spelled words by lexical distance
words = [(damerau_levenshtein_distance(word.decode('utf-8'), incorrectly_spelled_word.decode('utf-8')), word)
         for word in words]
words.sort()
words = [word for (editdistance, word) in words]

# trimming to top 30 entries
words = words[:30]

# getting definitions:
word_definitions = get_definitions(words) if words else []

if word_definitions:
    items = [{"title": word, "subtitle": definition, "arg": word} for word, definition in word_definitions]
else:
    items = [{"title": "no similar words found", "subtitle": "", "arg": incorrectly_spelled_word}]

output = {"items": items}

print(json.dumps(output, ensure_ascii=False))
