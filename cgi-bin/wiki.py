#!/usr/bin/env python3
from bs4 import BeautifulSoup
import cgi
import json
import requests as r
import re
from Errors import Errorobj

parameters = cgi.FieldStorage()
lang = parameters.getvalue("lang")
stop = parameters.getvalue("stop")
old = json.loads(parameters.getvalue("old"))
old = old["lijst"]
paths = []
error = Errorobj()


def nextlink(pagetitle, er: Errorobj):
    newlink = f"https://{lang}.wikipedia.org/wiki/" + pagetitle
    try:
        page = r.get(url=newlink)
    except r.RequestException or r.ConnectionError or r.ConnectTimeout:
        er.setError(True)
        er.setMessage("Verbinding mislukt")
        return None

    fsoup = BeautifulSoup(page.content, 'html.parser')
    # methode gevonden op stackoverflow maar vraag is verwijdert dus geen link
    changed = re.sub("\)", "</haakjes>", re.sub("\(", "<haakjes>", str(fsoup)))
    soup = BeautifulSoup(changed, 'html.parser')
    title = soup.find(id="firstHeading").text

    textblock = soup.find(id='bodyContent')
    all_par = textblock.find_all("p")
    # vind flattened list van alle links
    all_links = [a for p in all_par for a in
                 (p.find_all(lambda k: k.name == "a" and not k.find_parent("haakjes")))]

    scrapelink = ""
    for link in all_links:
        # check of link geen speciale wiki pagina
        if link['href'].find("/wiki/") != -1 and link["href"].find(":") == -1:
            scrapelink = link
            break

    if scrapelink == "":
        er.setError(True)
        er.setMessage("geen links gevonden")
    elif scrapelink["title"] in paths:
        er.setError(True)
        er.setMessage(
            f"lus gevonden bij {scrapelink['title']} zonder eindpunt te passeren")
    else:
        paths.append(title)
        return re.sub("</haakjes>", ")", (re.sub("<haakjes>", "(", str(scrapelink["title"]))))


modlink = nextlink(parameters.getvalue("start"), error)
while not error.getError() and modlink not in old:
    modlink = nextlink(modlink, error)

parent = str(modlink)
paths.reverse()

if error.getError():
    new_paths = {"error": error.getMessage()}
else:
    new_paths = {"paths": paths, "parent": parent}

print("Content-Type: application/json")
print()  # Lege lijn na headers
print(json.dumps(new_paths))
