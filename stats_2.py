from indexation import *
from math import *
import matplotlib.pyplot as plt


def req_treatment(req):
    doc =defaultdict(int)
    clean_req = re.split(r"[,/';().=!?\s]+", req)
    for word in clean_req:
        if len(word) > 1:
            doc[word] += 1
    return doc

def proba_bool_rank(req,k1,b):
    C = create_index()
    index = C
    C[req] = req_treatment(req)
    index_inverted = inversed_indexation_tf(C)
    similarity = []
    Q = C[req]

    avg_dl = 0
    for doc in index:
        avg_dl += sum(C[doc].values())
    avg_dl /= len(C) - 1
    for D in index:
        similarity.append((score(D, Q,index, index_inverted, avg_dl, k1,b), D))
    rank = sorted(similarity)
    rank.reverse()
    return rank



def score(D,Q, index, index_inversed,avg_dl,k1,b ):
    score = 0
    N = len(index)
    ld = sum(index[D].values())

    for q in Q:
        nq = len(index_inversed[q].keys())
        num2 = index[D][q]*(k1+1)*log(1+(N-nq+0.5)/(nq+0.5))
        denom2 = k1*(1-b+b*(ld/avg_dl))+index[D][q]

        score += num2/denom2

    return score


plt.close()
n = 10
l_k1 = [0.6 + 1.2*j/n for j in range(n+1) for  k in range(n+1)]
l_b = [k/n for  k in range(n+1)]*(n+1)
x = [k for k in range((n+1)**2)]
l_rappel = []
l_precision = []
req = "dieu grec"
doc_pert = ['output\\Hadès.txt', 'output\\Hermès.txt', 'output\\Apollon.txt',
                'output\\Zeus.txt', 'output\\Athéna.txt', 'output\\Poséidon.txt',
                'output\\Héra.txt', 'output\\Dionysos.txt']

for i in range((n+1)**2):

    print(str(round(100*i/(n+1)**2,2)) + "%")
    print(l_k1[i],l_b[i])
    rappel = []
    precision = []
    # à remplir à la main

    doc_renvoye = [url for similarity, url in proba_bool_rank(req, l_k1[i], l_b[i])]  # ensemble des docs renvoyé pas le sys
    doc_renvoye = doc_renvoye[1:40]

    R = len(doc_pert)
    doc_traite = []
    doc_pert_traite = []
    for url in doc_renvoye:
         doc_traite.append(url)
         if url in doc_pert:
             doc_pert_traite.append(url)
         A = len(doc_traite)
         Ra = len(doc_pert_traite)
         rappel.append(Ra / R)
         precision.append(Ra / A)
    l_rappel.append(rappel[-1])
    l_precision.append(precision[-1])


axes = plt.axes(projection = "3d")
axes.plot(l_k1, l_b, l_rappel)
axes.plot(l_k1, l_b, l_precision)
axes.set_xlabel("k1")
axes.set_ylabel("b")



plt.show()