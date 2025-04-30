from pathlib import Path
import re
from collections import defaultdict
from math import *

def process (fichier):
    doc = defaultdict(int)
    f = open(fichier, 'r', encoding = 'utf-8')
    contenu = f.read()
    if contenu == 'No extract found.' or contenu == "":
        return "error"
    #print(contenu)
    #print(type(contenu))
    f.close()

    clean_contenu = re.split(r"[,/';().=!?\s]+",contenu)
    for word in clean_contenu:
        if len(word) > 1:
            doc[word.lower()] += 1
    return doc


def create_index():
    #On extrait les fichiers et créer notre liste de document
    # Chemin du dossier
    dossier = Path('output')
    index = defaultdict(lambda : defaultdict(int))
    for fichier in dossier.iterdir():
        if fichier.is_file():
            document = process(fichier)
            if document != "error" :
                index[str(fichier)] = document
    return index

#print(create_index())



#print(create_index())

#print(repertory)


def inversed_indexation(index):
    inverted_index = defaultdict(lambda : defaultdict(int))

    for document in index:
        for mot in index[document]:
            inverted_index[mot.lower()][document] += 1
    return ponderation(index, inverted_index)



def l_pond(doc, word, max_tf):
    return 0.5 + 0.5 *(doc[word])/max_tf

def l_pond_1(doc, word ,max_tf):
    return doc[word]

def g_pond(word,inverted_index,N):
    return 1+log(N/len(inverted_index[word]))

def n_pond(doc, avg_doc_length):
    doc_length = sum(doc.values())
    pivot = 1.2
    slope = 0.75
    return (1+pivot)/(pivot*(1-slope)/slope)


def ponderation(index,inverted_index):
    max_tf = {doc :max(index[doc].values()) for doc in index}
    N = len(index.keys())
    avg_doc_length = 0
    for doc in index:
        avg_doc_length += sum(index[doc].values())
    avg_doc_length /= N

    for word in inverted_index:
        w_g = g_pond(word,inverted_index,N)
        for doc in inverted_index[word]:
            freq_t = l_pond(index[doc],word,max_tf[doc])*w_g*n_pond(index[doc], avg_doc_length)
            inverted_index[word][doc] = freq_t
    return inverted_index



#inversed_indexation(create_index(), big_repertory)
#print(inversed_indexation(create_index()))
