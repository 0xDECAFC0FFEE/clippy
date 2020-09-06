import json
from sys import argv, stderr
# import urllib.request
import urllib.parse
import ssl
import re
from typing import List, Tuple, Dict
import time
from httppool_client import wake_up_server, query_datamuse
# import datamuse_httppool_client

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

def parse_argv(argv: List[str]) -> Dict[str, str]:
    """converts argv to dict. 
    adds default max 4.
    adds spell as alternate command to sl.

    Args:
        argv (str): "sl macha ml tea"

    Returns:
        dict: argv converted into dictionary
    """
    if len(argv) == 1:
        wake_up_server()
        # datamuse_httppool_client.connect_to_server(datamuse_httppool_client.server_address)
        exit(0)
    inputs = argv[1].split(" ")

    args = dict(zip(inputs[::2], inputs[1::2]))
    if "spell" in args:
        args["sl"] = args["spell"]
        del args["spell"]
    args["max"] = args.get("max", "10")
    args["md"] = args.get("md", "") + "d"

    return args

def clean_datamuse_def(definition):
    if definition:
        return re.sub(r"([^(:?\t)]+)\t(.*)", r"\2", definition)
    else:
        return ""

api_args = parse_argv(argv)

query = urllib.parse.urlencode(api_args).lower()
response: List[dict] = json.loads(query_datamuse(query))
response = [word for word in response if "defs" in word][:6]
words = [word["word"] for word in response]
defs = [word.get("defs", [""])[0] for word in response]
defs = [clean_datamuse_def(definition) for definition in defs]

if "sl" in api_args:
    if api_args["sl"].title() == api_args["sl"]:
        words = [word.title() for word in words]
    titles = [(word if word.lower() != api_args["sl"].lower() else f"⭐ {word}") for word in words]
elif "sp" in api_args:
    if api_args["sp"].title() == api_args["sp"]:
        words = [word.title() for word in words]
    titles = [(word if word.lower() != api_args["sp"].lower() else f"⭐ {word}") for word in words]
else:
    titles = words

items = [{"title": title, "arg": word, "subtitle": defn} for title, word, defn in zip(titles, words, defs)]

output = {"items": items}
print(json.dumps(output, ensure_ascii=True))
