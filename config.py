# encoding: utf-8

# maximum number of characters in a definition
MAX_DEF_LEN = 200

# maximum time before server times out and shuts down
SERVER_TIMEOUT_SECONDS = 10

# modifies output of console if query is correctly spelled
def highlight_correctly_spelled_output(incorrectly_spelled_word, json_output):
    first_word = json_output[0]["title"]
    if first_word.lower() == incorrectly_spelled_word:
        json_output[0]["title"] = u"⭐ %s" % first_word
