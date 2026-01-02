import os
import json
import requests
from bs4 import BeautifulSoup
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
    out = None
    if "/doi/" in url:
        url = url.split("/doi/",1)
        return url[1]
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    for i in meta_names:
        meta = soup.find("meta", attrs={"name": i})
        if meta:
            return meta["content"].strip()  
    scripts = soup.find_all("script", type="application/ld+json")
    return ''.join([x for x in [DOIfrom_schemaorg(script) for script in scripts]])
def DOIfrom_schemaorg(script):
    try:
        data = json.loads(script.string)
    except Exception:
        pass
    if isinstance(data, list):
            for item in data:
                doi = extract_doi(item)
                if doi:
                    return doi
    else:
        doi = extract_doi(data)
        if doi:
            return doi
    return None

def extract_doi(data):
    if not isinstance(data, dict):
        return None

    # Common DOI locations
    if data.get("@type") == "ScholarlyArticle":
        identifier = data.get("identifier")
        if isinstance(identifier, dict):
            if identifier.get("propertyID", "").lower() == "doi":
                return identifier.get("value")

        if "doi" in data:
            return data["doi"]

    return None

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