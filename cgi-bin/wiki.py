#!/usr/bin/env python3
from bs4 import BeautifulSoup
import cgi
import json
import requests as r
import re
from Errors import Errorobj

parameters = cgi.FieldStorage()
lang = str(parameters.getvalue("lang"))
stop = str(parameters.getvalue("stop"))
#lang="nl"
#stop="Kennis"
paths = []
error = Errorobj()


def nextlink(pagetitle, er: Errorobj):
    newlink = f"https://{lang}.wikipedia.org/wiki/" + pagetitle
    try:
        page = r.get(url=newlink)
    except r.ConnectionError:
        er.setError(True)
        er.setMessage("Verbinding mislukt")

    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="firstHeading").text
    textblock = soup.find(id='bodyContent')
    all_par = textblock.find_all("p")
    all_links = [a for p in all_par for a in (p.find_all("a"))]

    scrapelink = ""
    for link in all_links:
        regex = re.compile(f"\([^()]*{link}[^()]*\)")
        if link['href'].find("/wiki/") != -1 and link["href"].find(":") == -1 \
                and not regex.search(str(textblock)):
            scrapelink = link
            break

    if scrapelink == '':
        er.setError(True)
        er.setMessage("geen links gevonden")
    elif scrapelink["title"] in paths:
        er.setError(True)
        er.setMessage("lus gevonden zonder eindpunt te passeren")
    else:
        paths.append(title)
        return str(scrapelink["title"])


modlink = nextlink(parameters.getvalue("start"), error)
#modlink = nextlink("Universiteit_Gent", error)
while modlink != stop and not error.getError():
    modlink = nextlink(modlink, error)

paths.append(stop)

if error.getError():
    new_paths = {"error": error.getMessage()}
else:
    new_paths = {"paths": paths}

print("Content-Type: application/json")
print()  # Lege lijn na headers
print(json.dumps(new_paths))
