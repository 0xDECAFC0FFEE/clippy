from tqdm import tqdm
import re
import os

# adding files in list of words
files = os.listdir("./words")
files = [file for file in files if re.match(".*\.txt", file)]
files = ["./words/%s" % file for file in files]

# adding words in unix dictionary to list of words
files.append("/usr/share/dict/words")

print("reading words from files")
words = set()
for file in tqdm(files):
    with open(file) as file_lines:
        for line in file_lines.readlines():
            if re.search("[^a-zA-Z0-9 _'\n-]", line):
                continue
            words.add(line[:-1].lower())

words = list(words)
words.sort()

print("writing words to words.txt")
with open("words.txt", "w+") as file:
    for word in tqdm(words):
        file.write("%s\n" % word)
