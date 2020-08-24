import json
from sys import argv, stderr
import urllib.request
import urllib.parse
import ssl
import re
from typing import List, Tuple, Dict

"""script that takes input from command line, queries datamuse and prints 
outputs formatted alfred style

inputs are formatted similar to how datamuse handles it
https://www.datamuse.com/api/

example inputs:

    sl macha ml tea
    "sounds like matcha, means like green"
    => matcha

    sp pipluup
    "spelled like pipluup"
    => piplup

    sl principle lc retired
    "sounds like principle, left context retired"
    => principal

    rel_syn down sl depresed
    "synonym to down, sounds like depresed"
    => depressed

    

Returns:
    [type]: [description]
"""


def parse_argv(argv: str) -> Dict[str, str]:
    """converts argv to dict. 
    adds default max 4.
    adds spell as alternate command to sl.

    Args:
        argv (str): "sl macha ml tea"

    Returns:
        dict: argv converted into dictionary
    """
    if len(argv) == 1:
        exit(0)
    inputs = argv[1].split(" ")

    args = dict(zip(inputs[::2], inputs[1::2]))
    if "spell" in args:
        args["sl"] = args["spell"]
        del args["spell"]
    args["max"] = args.get("max", "4")

    return args

def query_datamuse(api_args: str) -> Tuple[List, List]:
    """handles api call to datamuse servers

    Args:
        api_args (dict): args to api call

    Returns:
        
    """
    url = f"https://api.datamuse.com/words?{urllib.parse.urlencode(args)}"
    incorrectly_spelled_word = str(argv[1]).lower()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(url, context=ctx) as response:
        response = json.loads(response.read().decode("latin-1"))
        words = [word["word"] for word in response]
        defs = [word.get("defs", [""])[0] for word in response]

    return words, defs

def clean_datamuse_def(definition):
    if definition:
        return re.sub(r"([^(:?\t)]+)\t(.*)", r"\2", definition)
    else:
        return ""

args = parse_argv(argv)
words, defs = query_datamuse(args)
defs = [clean_datamuse_def(definition) for definition in defs]

if "sl" in args:
    titles = [(word if word != args["sl"] else f"⭐ {word}") for word in words]
else:
    titles = words

items = [{"title": title, "arg": word, "subtitle": defn} for title, word, defn in zip(titles, words, defs)]

output = {"items": items}
print(json.dumps(output, ensure_ascii=True))
