import re
import os

files = []
for file in os.listdir("."):
    if re.match("words[0-9].txt", file):
        files.append(file)

files.append("/usr/share/dict/words")
words = set()
for file in files:
    with open(file) as file_lines:
        for line in file_lines.readlines():
            if not re.search("[^a-zA-Z0-9 _'\n-]", line):
                words.add(line[:-1])
        print("finished reading file %s" % file)

words = list(words)
words.sort()
with open("words.txt", "w+") as file:
    for word in words:
        file.write(word)
        file.write("\n")
