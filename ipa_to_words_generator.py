from metaphone import doublemetaphone
from DictionaryServices import *
from collections import defaultdict
import dbm

print("retrieving words")
osx_words = []
with open("words.txt", "r") as readFile:
    for line_raw in readFile.readlines():
        osx_words.append(line_raw[:-1].lower())

print("filtering out words not in osx dictionary")
new_oxford_american_dictionary_words = []
for osx_word in osx_words:
    wordrange = (0, len(osx_word))
    dictresult = DCSCopyTextDefinition(None, osx_word, wordrange)
    if dictresult:
        new_oxford_american_dictionary_words.append(osx_word)

print("transposing dictionary")
ipa_to_words = defaultdict(lambda: [])
for word in new_oxford_american_dictionary_words:
    for ipa in doublemetaphone(word):
        if ipa != "":
            ipa_to_words[ipa].append(word)

print("adding words to on database")
with dbm.ndbm.open("ipa_to_words", "n") as database:
    for word, ipas in ipa_to_words.items():
        database[word] = " ".join(ipas)
