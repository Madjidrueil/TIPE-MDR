from Indexation import *
from math import *
import matplotlib.pyplot as plt


def scal(req, doc,C, index_inverted):
    s = 0
    for word in C[req]:
        if doc in index_inverted[word]:
            s += index_inverted[word][req]*index_inverted[word][doc]
    return s

def norm(d,C,index_inverted):
    s = 0
    for word in C[d]:
        s += index_inverted[word][d]**2
    return sqrt(s)

def vect_rank():
    query = input("balance la requête : ")
    if query == "" : #sécurité
        return "incorrect query"
    C = create_index()  #On crée l'index
    C[query] = query_treatment(query)     #Corpus = Index U query
    index_inverted = inversed_indexation_tf_idf(C) # type de pondération (à mettre à la main)
    similarity = [] #Tableau de similarité

    query_norm = norm(query,C, index_inverted)
    #On ajoute à similarité (cos(angle(di,query)),di)
    for url in C:
        di_norm = norm(url,C, index_inverted) # Norme de di (le vecteur)
        scal_di = scal(query, url,C,index_inverted)
        if di_norm != 0:    #sécurité
            similarity.append((scal_di/(di_norm*query_norm), url))
        else:
            similarity.append(("erreur",url))
    rank = sorted(similarity)
    rank.reverse()
    return rank

def relevant_doc():
    relevant = []
    vu = []
    cond = input("doc à remplir (sinon taper 'STOP') : ")
    while cond != 'STOP':
        if not(cond in vu):
            relevant.append(str(directory)+"\\"+cond+".txt")
            vu.append(cond)
        cond = input("doc à remplir (sinon taper 'STOP') : ")
    return relevant

def recall_precision(proportion):
    plt.close()

    rank = vect_rank()
    recall = []
    precision = []
    treated_doc = []
    treated_rel_doc = []

    relevant_docs = relevant_doc()
    doc_renvoye = [url for similarity, url in rank]  # ensemble des docs renvoyé pas le sys
    doc_renvoye = doc_renvoye[1:round(proportion*len(rank), 0)]
    R = len(relevant_docs)

    for url in doc_renvoye: #établissement des courbes rappel-precision à proportion
        treated_doc.append(url)
        if url in relevant_docs:
            treated_rel_doc.append(url)
        A = len(treated_doc)
        Ra = len(treated_rel_doc)
        recall.append(Ra / R)
        precision.append(Ra / A)
    plt.plot(recall[1:], precision[1:])
    plt.show()





recall_precision(0.1)
