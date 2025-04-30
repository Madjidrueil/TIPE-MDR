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

def scal(req, d,C, index_inverted):
    s = 0
    for word in C[req]:
        if d in index_inverted[word]:
            s += index_inverted[word][req]*index_inverted[word][d]
    return s

def norme(d,C,index_inverted):
    s = 0
    for word in C[d]:
        s += index_inverted[word][d]**2
    return sqrt(s)

def vect_rank():
    req = input("balance la requête : ")
    C = create_index()
    C[req] = req_treatment(req)
    index_inverted = inversed_indexation(C)
    similarity = []

    norme_req = norme(req,C, index_inverted)
    for url in C:
        norme_di = norme(url,C, index_inverted)
        scal_di = scal(req, url,C,index_inverted)
        #print(scal_di, norme_di)
        if norme_di != 0:
            similarity.append((scal_di/(norme_di*norme_req), url))
        else:
            similarity.append((0,url))
    rank = sorted(similarity)
    rank.reverse()
    print(rank)
    return rank





#code
plt.close()

rappel = []
precision = []

#à remplir à la main
doc_pert = ['output\\Hadès.txt', 'output\\Hermès.txt','output\\Apollon.txt',
            'output\\Zeus.txt','output\\Athéna.txt', 'output\\Poséidon.txt',
            'output\\Héra.txt', 'output\\Dionysos.txt'] #
doc_renvoye = [url for similarity, url in vect_rank()] #ensemble des docs renvoyé pas le sys
doc_renvoye = doc_renvoye[:]

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

