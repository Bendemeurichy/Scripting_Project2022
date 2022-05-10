#!/usr/bin/env python3
import cgi
import json

import requests as r
from bs4 import BeautifulSoup

baselink = ".wikipedia.org/wiki"
#parameters = cgi.FieldStorage()

#modlink = "https://" + parameters.getvalue("lang") + baselink + parameters.getvalue("start")
#stop=parameters.getvalue("stop")

#page = r.get(modlink)
page=r.get("https://en.wikipedia.org/wiki/Special:Random")
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.find(id="firstHeading")
textblock = soup.find(id='bodyContent')
link = soup.find(id='bodyContent').find("p").find_all("a")
print(link[0]["href"])
