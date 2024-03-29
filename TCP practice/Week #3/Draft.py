import json

with open("settings.json", 'r') as file:
    SETTINGS = json.load(file)
print("file loaded")
linkLists = SETTINGS["linkLists"]
linkNum = SETTINGS["linkNum"]
nodeLists = SETTINGS["nodeLists"]

s = nodeLists[1]["socket"]