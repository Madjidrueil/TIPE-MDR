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




def proba_bool_rank():
    req = input("balance la requête : ")
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
        similarity.append((score(D, Q,index, index_inverted, avg_dl), D))
    rank = sorted(similarity)
    rank.reverse()
    return rank



def score(D,Q, index, index_inversed,avg_dl ):
    score = 0
    k1, b = 1.2,  0.75
    N = len(index)
    ld = sum(index[D].values())

    for q in Q:
        nq = len(index_inversed[q].keys())
        num2 = index[D][q]*(k1+1)*log(1+(N-nq+0.5)/(nq+0.5))
        denom2 = k1*(1-b+b*(ld/avg_dl))+index[D][q]

        score += num2/denom2

    return score


#code
plt.close()

rappel = []
precision = []

#à remplir à la main
doc_pert = ['output\\Hadès.txt', 'output\\Hermès.txt','output\\Apollon.txt',
            'output\\Zeus.txt','output\\Athéna.txt', 'output\\Poséidon.txt',
            'output\\Héra.txt', 'output\\Dionysos.txt'] #
doc_renvoye = [url for similarity, url in proba_bool_rank()] #ensemble des docs renvoyé pas le sys
doc_renvoye = doc_renvoye[1:20]

R = len(doc_pert)
doc_traite = []
doc_pert_traite = []
for url in doc_renvoye:
    doc_traite.append(url)
    if url in doc_pert:
        doc_pert_traite.append(url)
    A = len(doc_traite)
    Ra = len(doc_pert_traite)
    rappel.append(Ra/R)
    precision.append(Ra/A)
print(precision[-1], rappel[-1])

plt.plot(rappel[1:], precision[1:])
plt.show()
