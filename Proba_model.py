from Indexation import *
from math import *
import matplotlib.pyplot as plt
from time import*

def proba_rank():
    query = input("balance la requête : ")
    if query == "":  # sécurité
        return "incorrect query"
    C = create_index()  # On crée l'index
    N = len(C)
    C[query] = query_treatment(query)  # Corpus = Index U query
    index_inverted = inversed_indexation_tf(C)  # type de pondération (à mettre à la main)
    similarity = []  # Tableau de similarité
    avg_dl = 0
    for doc in (C):
        avg_dl += sum(C[doc].values())
    avg_dl /= len(C) - 1

    for doc in C:
        similarity.append((score(doc,C[query],C,avg_dl,index_inverted,N), doc))
    similarity.remove((score(query,C[query],C,avg_dl,index_inverted,N), query))
    rank = sorted(similarity)
    rank.reverse()
    print(rank)
    return rank

def score(doc,Q, C,avg_dl,index_inverted,N ):
    score = 0
    k1, b = 1.2,  0.75
    ld = 0
    for word in C[doc]:
        ld += C[doc][word]

    for q in Q:
        tf = C[doc][q]
        df = len(index_inverted[q].keys())

        num = tf*(k1+1)
        denom = k1*(1-b+b*(ld/avg_dl))+tf
        ln = log((N-df+0.5)/(df + 0.5))

        score +=  num * ln/(denom)
    return score


def relevant_doc():
    relevant = []
    vu = []
    #cond = ["facebook", "instagram", "snapchat", "telegram (application)", "tik tok", "STOP"]
    cond = ["badminton","coupe du monde","escalade","football","jeux olympiques","judo",
"rugby","squash","taekwondo","tennis","voile","vélo","équitation","bobsleigh","escrime",
            "parcours","curling","nike", "adidas","STOP" ]
    #cond = input("doc à remplir (sinon taper 'STOP') : ")
    i = 0
    while cond[i] != 'STOP':
        if not(cond[i] in vu):
            relevant.append(str(directory)+"\\"+cond[i].lower()+".txt")
            vu.append(cond[i])
        #cond = input("doc à remplir (sinon taper 'STOP') : ")
        i += 1
    return relevant

def recall_precision(proportion):
    a = time()

    plt.close()
    rank = proba_rank()
    recall = []
    precision = []
    treated_doc = []
    treated_rel_doc = []
    relevant_docs = relevant_doc()
    doc_renvoye = [url for similarity, url in rank]  # ensemble des docs renvoyé pas le sys
    doc_renvoye = doc_renvoye[:int(round(proportion*len(rank), 0))]
    print(len(doc_renvoye))
    R = len(relevant_docs)

    for url in doc_renvoye: #établissement des courbes rappel-precision à proportion
        treated_doc.append(url)
        if url in relevant_docs:
            treated_rel_doc.append(url)
        A = len(treated_doc)
        Ra = len(treated_rel_doc)
        recall.append(Ra / R)
        precision.append(Ra / A)

    plt.plot(recall[1:], precision[1:], color = "green")
    plt.xlabel('recall')
    plt.ylabel('precision')
    print(time()-a)
    plt.show()
    return (recall[-1], precision[-1])

print(recall_precision(0.03))