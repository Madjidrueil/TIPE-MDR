from Indexation import *
from math import *
import matplotlib.pyplot as plt

plt.close()

def proba_rank(k1,b):
    query = "sport"
    if query == "":  # sécurité
        return "incorrect query"
    C = create_index()  # On crée l'index
    C[query] = query_treatment(query)  # Corpus = Index U query
    index_inverted = inversed_indexation_tf(C)  # type de pondération (à mettre à la main)
    similarity = []  # Tableau de similarité
    avg_dl = 0
    for doc in (C):
        avg_dl += sum(C[doc].values())
    avg_dl /= len(C) - 1

    for doc in C:
        similarity.append((score(doc,C[query],C,avg_dl,index_inverted,k1,b), doc))
    similarity.remove((score(query,C[query],C,avg_dl,index_inverted,k1,b), query))
    rank = sorted(similarity)
    rank.reverse()
    print(rank)
    return rank

def score(doc,Q, C,avg_dl,index_inverted,k1,b):
    score = 0
    ld = 0
    for word in C[doc]:
        ld += C[doc][word]
    N = len(C)

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

def recall_precision(proportion,k1,b):

    rank = proba_rank(k1,b)
    recall = []
    precision = []
    treated_doc = []
    treated_rel_doc = []
    relevant_docs = relevant_doc()
    doc_renvoye = [url for similarity, url in rank]  # ensemble des docs renvoyé pas le sys
    doc_renvoye = doc_renvoye[1:int(round(proportion*len(rank), 0))]
    R = len(relevant_docs)

    for url in doc_renvoye: #établissement des courbes rappel-precision à proportion
        treated_doc.append(url)
        if url in relevant_docs:
            treated_rel_doc.append(url)
        A = len(treated_doc)
        Ra = len(treated_rel_doc)
        recall.append(Ra / R)
        precision.append(Ra / A)

    return (recall[-1], precision[-1])


k1= 0
x = []
a = 10
c = 10
recall_glob = []
precision_glob = []
for i in range(1,a+1):
    b = 0
    k1 = 1.2*2*i/(a+1)
    for j in range(1,c+1):
        b = 0.75*2*j/(c+1)
        print(str(10*(-1+i)+j-1)+"% ;"+" k1 : " +str(k1) + " b : " +str(b))
        if k1 != 0 and b != 0:
            x.append(10*(i-1)+(j-1))
            temp = recall_precision(0.1,k1,b)
            recall_glob.append(temp[0])
            precision_glob.append(temp[1])


axes = plt.axes(projection = "3d")
axes.plot(x, recall_glob, precision_glob)
axes.set_xlabel("x")
axes.set_ylabel("recall")
axes.set_zlabel("precision")

print(recall_glob)
print(precision_glob)
plt.show()


