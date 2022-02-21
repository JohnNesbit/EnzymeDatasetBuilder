import numpy as np
import get_links
import tqdm
import os

try:
    os.mkdir("aa")
    os.mkdir("ec")
except:
    pass

sequence_size = 200
pages = 10

transcriptionstr = "QWERTYUIOPASDFGHJKLZXCVBNM"
print(len(transcriptionstr))
transcription_table = dict(zip(list(transcriptionstr), range(len(transcriptionstr))))

# get aa and chemical names, structure if possible
links = []
for j in range(pages):
    links = links + list(
        get_links.get_links("https://www.uniprot.org/uniprot/?query=enzyme" + "&offset=" + str(j * 25)))

# find working links: eliminate all of the extraneous links on the webpage
legit_links = []
for i in links:
    if "https://www.uniprot.org/uniprot/" in i and i != "https://www.uniprot.org/uniprot/":
        if "taxononmy" and "help" and "query" not in i:
            legit_links.append(i)


aa = []

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request


# get visible elements
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# get the visible text from the page
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

import re

broken = 0
last = 0
gots = 39

# initialize iterator that shows progress
t = tqdm.tqdm(legit_links)

# loop through links and get the ammino acid sequences for each enzyme.
for elink in t:
    ecList = []
    aa = []
    enzyme_page = 0
    
    # get body text. aa sequence starts after SV number, so just throw out anything with a number after it + numbers
    html = urllib.request.urlopen(elink + ".fasta").read()
    try:
        nhtml = str(urllib.request.urlopen(elink).read())
    except IndexError:
        continue
    name = str(nhtml.split('<h1 property="name">')[1].split('</h1>')[0])
    name = name.replace(" ", "")

    if "/" in name or "\\" in name or "[" in name:
        continue

    try:
        text = str(str(html))
        text = text.split('\\n')[1:]
        text = ''.join(text)
        text.replace('\\n', '')
    except:
        print("BioCyc Error")

    tex = []
    for char in text:
        if char in transcriptionstr:
            tex.append(char)
    text = np.array([transcription_table[a] for a in tex])



    link = 'https://biocyc.org/META/substring-search?type=NIL&object=' + name +'&quickSearch=Quick+Search'
    #print(link)

    html2 = str(urllib.request.urlopen(link).read())

    if 'Gene-Reaction Schematic' not in html2:

        try:
            prelink = html2.split("/gene?orgid")[1]
        except IndexError:
            continue

        enzyme_page = 'https://biocyc.org/gene?orgid' + str(prelink.split('">')[0])

        if '\\' in enzyme_page:
            enzyme_page = enzyme_page.split("\\")[0]


        ol = str(urllib.request.urlopen(enzyme_page).read())
    else:
        ol = str(urllib.request.urlopen(link).read())

    try:
        EC_page = "https://biocyc.org/META/NEW-IMAGE?type=REACTION" + str(ol.split("/META/NEW-IMAGE?type=REACTION")[1].split('"')[0])
    except IndexError:
        continue

    aa.append(text)
    ecList.append([EC_page, elink])


    aah = []
    for i in range(sequence_size):
        try:
            aah.append(aa[i])
        except IndexError:
            aah.append(27)

    aah = np.array(aah)

    gots += 1

    np.save("aa/aa" + str(gots) + ".npy", np.array(aah).reshape([sequence_size]))
    np.save("ec/ec" + str(gots) + ".npy", ecList)

    t.set_description_str(str(gots))
