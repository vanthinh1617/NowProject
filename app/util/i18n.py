import i18n, os
from flask import request
from pathlib import Path
i18n.set("fallback", "en")
i18n.set("locale", "vi")
def run(path):
    i18n.load_path.append(path)

def setLocalte(lang):
    checkValid(lang)
    i18n.set("locale", lang)
    
def checkValid(lang):
    valids = ['vi', 'en']
    if lang not in valids: raise "invalid request header!"

def beforeRequest():
    lang = request.headers.get('x-food-client-language')
    if lang is None:
        lang = 'vi'
    else:
        checkValid(lang)
    setLocalte(lang)