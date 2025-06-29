import requests
import numpy as np
from Vect_model import vect_rank
from Crawler import directory
from time import *
import matplotlib.pyplot as plt


def get_links(page_title, lang='fr'):

    base_url = f"https://{lang}.wikipedia.org/w/api.php"
    links = []
    params = {
        'action': 'query',
        'prop': 'links',
        'titles': page_title,
        'format': 'json'}

    while True:
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page in pages.values():
                links.extend([link['title'] for link in page.get('links', [])])

            if 'continue' in data:
                params.update(data['continue'])
                sleep(0.1)  # Respect des limites de requête
            else:
                break

        except Exception as e:
            print(f"Erreur: {e}")
            break

    return links

def uniforme_matrice(M): # M est un tab numpy
    uniform_M = np.array([[0. for i in range (len(M))] for j in range(len(M))])
    for i in range(len(M)):
        norme = 0
        cond = False
        s = 0
        max_non_nul = 0
        for j in range(len(M)):
            norme += M[i][j]
        if norme == 0:
            norme = 1
            cond = True
        for j in range(len(M)):
            uniform_M[i][j] = round(M[i][j]/norme,2)
            if uniform_M[i][j] != 0:
                max_non_nul = j
                s += uniform_M[i][j]
        uniform_M[i][max_non_nul] += 1 - s
        if cond:
            for j in range(len(M)):
                uniform_M[i][j] = round(1/len(M),2)
    return uniform_M

def Markov(P):
    n = P.shape[0]
    A = np.transpose(P) - np.eye(n)
    A = np.vstack((A, np.ones(n)))  # contrainte somme(pi) = 1
    b = np.zeros(n + 1)
    b[-1] = 1
    pi, residual, rank, s = np.linalg.lstsq(A, b, rcond=None)
    pi = pi / pi.sum()
    return pi

def Page_Rank():
    result = vect_rank()[1:20]
    print(result)
    valid_links = []
    for url in result:
        title = url[1].replace(str(directory)+"\\", "")
        valid_links.append( title.replace('.txt', ""))
    conv = {valid_links[i] : i for i in range(len(valid_links))}
    M_adj = np.array([[0 for i in valid_links] for j in valid_links])
    for title in valid_links:
        print(title)
        links = get_links(title)
        for link in links:
            if link.lower() in valid_links:
                M_adj[conv[title]][conv[link.lower()]] += 1
    print(M_adj)
    u_M = uniforme_matrice(M_adj)
    print(u_M)
    pi = Markov(u_M)
    popularity = []
    for i in range(len(pi)):
        popularity.append((abs(pi[i]),i))
    rank = sorted(popularity)
    print(rank)
    rank.reverse()
    return [result[doc_number[1]][1] for doc_number in rank]

def relevant_doc():
    relevant = []
    vu = []
    cond = ["badminton","coupe du monde","escalade","football","jeux olympiques","judo",
"rugby","squash","taekwondo","tennis","voile","vélo","équitation","bobsleigh","escrime",
            "parcours","curling","nike","adidas","STOP" ]
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
    plt.close()

    rank = Page_Rank()
    print(rank)
    recall = []
    precision = []
    treated_doc = []
    treated_rel_doc = []

    relevant_docs = relevant_doc()
    doc_renvoye = [url for url in rank]  # ensemble des docs renvoyé pas le sys
    print(int(round(proportion*len(rank), 0)))
    #doc_renvoye = doc_renvoye[1:10]
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
    plt.plot(recall[1:], precision[1:], color = "blue")
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.show()
    print(recall[-1], precision[-1])

recall_precision(0.5)