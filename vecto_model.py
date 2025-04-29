from indexation import *
from math import *


def traitement(req):
    doc = []
    clean_req = re.split(r"[,/';().=!?\s]+", req)
    for word in clean_req:
        if len(word) > 1:
            doc.append(word.lower())
    return doc

def scal(d0, di ,rep0, repi,index_inverted):
    s = 0
    for word in d0:
        if repi in index_inverted[word]:

            s += index_inverted[word][rep0]*index_inverted[word][repi]
    return s

def norme(d1,index_inverted, rep1):
    s = 0
    for word in d1:
        s += index_inverted[word][rep1]**2
    return sqrt(s)

def main():
    req = input("balance la requête")
    C = [traitement(req)] + create_index()
    rep = [req] + big_repertory

    index_inverted = inversed_indexation(C,rep)
    #print(index_inverted)

    rank = []
    similarity = []
    norme_req = norme(traitement(req),index_inverted, req)
    for i in range(1,len(C)):
        norme_di = norme(C[i], index_inverted, rep[i])
        scal_di = scal(C[0], C[i],rep[0], rep[i],index_inverted)
        #print(scal_di, norme_di)
        if norme_di != 0:
            similarity.append(scal_di/(norme_di*norme_req))
        else:
            similarity.append(0)
    print(similarity)

print(main())