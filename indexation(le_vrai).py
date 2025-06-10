from pathlib import Path
import re
from collections import defaultdict
from math import *
from Crawler import directory

def create_index():
    root = Path(directory)  #nom du dossier
    index = defaultdict(lambda : defaultdict(int))  #initialisation de l'index
    for file in root.iterdir(): #Pour ajouter chaque documents à l'index
        if file.is_file():
            document = process(file)
            if document != "error" :    #2ème sécurité pour n'avoir que des docs non-vides
                index[str(file).lower()] = document
    print(len(index))
    return index

def process (file):
    doc = defaultdict(int)  #initialisation du vecteur di
    #On ouvre le texte et ajoute son contenu dans "content"
    f = open(file, 'r', encoding = 'utf-8')
    content = f.read()
    if content == 'No extract found.' or content == "":
        return "error"
    f.close()

    #On nettoie le fichier et représente le vecteur di
    clean_content = re.split(r"[,/';().=!?\s]+",content)
    for word in clean_content:
        if len(word) > 1 and not(word in useless_words):
            doc[word.lower()] += 1
    return doc



useless_words = ["le", "de", "un", "être", "et", "il", "avoir", "ne", "je", "son", "la",
                 "que", "se", "qui", "ce", "dans", "en", "du", "elle", "au", "pour", "par"]

def ponderation_tf_idf(index,inverted_index):
    N = len(index.keys())
    for word in inverted_index:
        w_g = 1+log(N/len(inverted_index[word]))
        for doc in inverted_index[word]:
            freq_t = index[doc][word]* w_g
            inverted_index[word][doc] = freq_t
    return inverted_index

def inversed_indexation_tf_idf(index):
    inverted_index = defaultdict(lambda : defaultdict(int))
    for document in index:
        for mot in index[document]:
            inverted_index[mot.lower()][document] += 1
    return ponderation_tf_idf(index, inverted_index)

def query_treatment(req):
    doc =defaultdict(int)
    clean_query = re.split(r"[,/';().=!?\s]+", req)
    for word in clean_query:
        if len(word) > 1:
            doc[word.lower()] += 1
    return doc
