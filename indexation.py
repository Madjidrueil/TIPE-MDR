from collections import defaultdict
from pathlib import Path
import re
from collections import defaultdict


big_repertory = []

def create_index():
    #On extrait les fichiers et créer notre liste de document
    # Chemin du dossier
    dossier = Path('output')
    index = []

    for document in dossier.iterdir():
        if document.is_file():
            big_repertory.append(str(document))
            index.append(process(document))

    return index


def process (fichier):
    doc = []
    f = open(fichier, 'r', encoding = 'utf-8')
    contenu = f.read()
    #print(contenu)
    #print(type(contenu))
    f.close()

    clean_contenu = re.split(r"[,/';().=!?\s]+",contenu)
    for word in clean_contenu:
        if len(word) > 1:
            doc.append(word)
    return doc

#print(create_index())


#print(repertory)


def inversed_indexation(index,repertory):
    inverted_index = defaultdict(lambda : defaultdict(int))

    for i in range(len(index)):
        for mot in index[i]:
            inverted_index[mot.lower()][repertory[i]] += 1
    return inverted_index

#print(inversed_indexation(create_index(), big_repertory))