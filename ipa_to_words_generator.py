from metaphone import doublemetaphone
from DictionaryServices import *
from collections import defaultdict
from defaultlist import defaultlist
import hashlib
import pprint

osx_words = []
with open("words.txt", "r") as readFile:
    for line_raw in readFile.readlines():
        osx_words.append(line_raw[:-1].lower())

print("retrieved words")

new_oxford_american_dictionary_words = []
for osx_word in osx_words:
    wordrange = (0, len(osx_word))
    dictresult = DCSCopyTextDefinition(None, osx_word, wordrange)
    if dictresult:
        new_oxford_american_dictionary_words.append(osx_word)

print("filtered out words not in osx dictionary")

ipa_to_words = defaultdict(lambda: [])
for word in new_oxford_american_dictionary_words:
    for ipa in doublemetaphone(word):
        if ipa != "":
            ipa_to_words[ipa].append(word)

ipa_to_words_hashtable_size = int(len(ipa_to_words) * 3 / 4)
print("%s entries" % ipa_to_words_hashtable_size)

new_english_word_entries = defaultlist(lambda: [])
for metaphoneme, line in ipa_to_words.items():
    m = hashlib.md5()
    m.update(str.encode(metaphoneme))
    new_english_word_entries[int(m.hexdigest(), 16) %
                             ipa_to_words_hashtable_size].append((metaphoneme, line))

pprint.pprint(new_english_word_entries)

max_entry_length = 0

entries = []
for new_english_word_entry in new_english_word_entries:
    entrytext = ""
    for metaphoneme, words in new_english_word_entry:
        entrytext+="|%s " % metaphoneme
        for word in words:
            entrytext+="%s " % word
    entries.append(entrytext)

    if len(entrytext) > max_entry_length:
        max_entry_length = len(entrytext)

print("REMEMBER TO CHANGE LINE LENGTH TO %d" % (max_entry_length+1))
print("REMEMBER TO CHANGE HASH MOD VALUE TO %d" % ipa_to_words_hashtable_size)
for index, entry in enumerate(entries):
    entries[index] = entry.ljust(max_entry_length, " ")

open("ipa_to_words.txt", "w").close()
with open("ipa_to_words.txt", "a") as writeFile:
    for entry in entries:
        writeFile.write(entry)
        writeFile.write("\n")
