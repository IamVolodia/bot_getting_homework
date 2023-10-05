import json

def LEXICON():
    with open('lexicon//lexicon.json', encoding='utf-8') as file:
        templates = json.load(file)
    return templates