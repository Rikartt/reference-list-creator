import os
import json
import requests
from bs4 import BeautifulSoup
import re

DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s\"<>]+)", re.I)
#read input.txt and output an alphabetically ordered list without potential fluff.
def readtxt(file):
    cwd = os.getcwd()
    with open(f'{cwd}/IO/{file}.txt', 'r') as f:
        txt = f.read()
        f.close()
    txt = [''.join(c for c in x.strip() if c not in ' "<>#%{}|\\^~[]`()') for x in txt.split(' ') if "http" in x]
    txt.sort()
    return txt
#try to get the DOI
def getDOI(url):
    meta_names = ["citation_doi", "publication_doi","dc.Identifier"]
    out = DOI_RE.search(url)
    if out:
        return out.group(1)
    else:
        html = requests.get(url,
            headers={"User-Agent": "DOI-finder/1.0"},
            timeout=20).text
        soup = BeautifulSoup(html, "html.parser")
        if soup.head:
            headtext = soup.head.getText(" ",strip=True)
            out = DOI_RE.search(str(headtext))
    if out:
        return out.group(1)
    #for i in meta_names:
    #    meta = soup.find("meta", attrs={"name": i})
    #    if meta:
    #        return meta["content"].strip() 
    #    meta =  soup.find("meta", attrs={"property": i})
    #    if meta:
    #        return meta["content"].strip()
DOI_list = []
url_list = readtxt("input")
ref_list = []
def urlprotocol(element): #What to do to each url
    DOI = getDOI(element)
    if DOI:
        return DOI_list.append(DOI)
def enscribe(list, filename):
    cwd = os.getcwd()
    with open(f'{cwd}/IO/{filename}.txt','w') as f:
        f.write('\n'.join(list))
        f.close()
[urlprotocol(x) for x in url_list]
enscribe(DOI_list, "DOI_list")