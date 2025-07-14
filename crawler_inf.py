from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
import re
from Models_bdd_inf import *
import requests
from time import *
#--------------------------------------------------------------------------------------
#                             ---Fonctions---
def get_links_api(page_title, limit ,lang='fr'):
    """
    Récupère tous les liens d'une page Wikipédia via l'API
    :param page_title: Titre de la page Wikipédia (avec _ pour les espaces)
    :param lang: Langue de Wikipédia (fr, en, etc.)
    :return: Liste des liens trouvés
    """
    base_url = f"https://{lang}.wikipedia.org/w/api.php"
    links = []

    params = {
        'action': 'query',
        'prop': 'links',
        'titles': page_title,
        'format': 'json'
    }

    while True:
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            #print(pages)
            for page in pages.values():
                for link in page.get('links', []):
                    if len(links) > limit :
                        return links
                    else:
                        if not([link['title']] in deja_vu) and link["title"][0] != ".":
                            links.extend([link['title']])
            if 'continue' in data:
                params.update(data['continue'])
                sleep(0.1)  # Respect des limites de requête
            else:
                break

        except Exception as e:
            print(f"Erreur: {e}")
            break

    return links


def valid_url(titles):
    valid_urls = []
    i = 0
    for title in titles:
        i += 1/len(titles)
        print(str(i*100)+"%")
        url = f"https://fr.wikipedia.org/w/api.php"
        params_text = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'explaintext': True,
            'titles': title}
        response = requests.get(url, params=params_text)
        if response.status_code == 200:
            data = response.json()
            pages = data['query']['pages']
            page = next(iter(pages.values()))
            if type(page.get('extract')) == str and (not title in valid_urls) :
                content = page.get('extract')
                valid_urls.append(title)
                print(title)
                save_to_bdd(title,content)
            else:
                print(title)
        else:
            raise Exception(f"HTTP Error: {response.status_code}")
    return valid_urls

def save_to_bdd(title, content):
    temp_dict = defaultdict(int)
    if content != "error" and content != "":
        Session = sessionmaker(bind=engine)
        session = Session()
        document = Index(document=title)
        session.add(document)
        clean_content = re.split(r"[,/';().=!?\s]+", content)
        for word in clean_content:
            if len(word) > 1 and not (word.lower() in useless_words):
                temp_dict[word.lower()] += 1
        #i,N = 0, len(temp_dict)
        for word in temp_dict:
            #print(str(round(100*i/N,1)) + "%")
            #i += 1
            W = Index_inverse(word_id = word, document = title, word_freq = temp_dict[word])
            session.add(W)
            distinct_word = session.query(Répertoire).all()
            if word in distinct_word:
                distinct_word.word_freq = distinct_word.word_freq + temp_dict[word]
            else:
                session.add(Répertoire(word_id = word,word_freq = temp_dict[word]))

        session.commit()


def crawl(titles):
    ti = time()
    print("Step 1")
    sleep(0.5)
    valid_url(titles)
    print("temps step 1 : " + str(time() - ti))
    print("end_scrapper")

def no_links():
    file = []
    index =session.query(Index).all()
    deja_vu = index
    infini = 1000000000
    while index != [] or len(file) != 20:
        doc = index.pop()
        liens = get_links_api(doc, infini)
        for lien in liens:
            if not(lien in deja_vu):
                file.append(lien)
    if file != []:
        return file
    return "Error, no more links found"
#--------------------------------------------------------------------------------------
#                           ---Code---

useless_words = ["le", "de", "un", "être", "et", "il",
                 "avoir", "ne", "je", "son", "la",
                 "que", "se", "qui", "ce", "dans", "en",
                 "du", "elle", "au", "pour", "par"]



db_url = 'sqlite:///bdd_inf.db'
engine = create_engine(db_url)
deja_vu = []
titles = []
file = []

try:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    #initialisation des données
    Session = sessionmaker(engine)
    session = Session()
    len_File = session.query(Info).filter(Info.nb_doc_file).first() #len(File)
    if len_File == None: len_File = 0
    for i in range(len_File):
        q_i = session.query(File).filter(id == i).first() #Doc numéro i de la pile
        titles.append(q_i)
    len_index = session.query(Info).filter(Info.nb_doc).first() #len(Index)
    if len_index == None:
        len_index = 0
        titles = ["France"] #On initialise les titres s'il n'y a plus rien dans la pile
    for i in range(len_index):
        q_i = session.query(Index).filter(id == i).first() #Doc numéro i de l'index
        deja_vu.append(q_i)
    print(titles, deja_vu)

    while input("STOP : ") != "STOP":
        for title in titles:
            taille_file = 20
            while len(file) <= taille_file:
                file = file + get_links_api(page_title = title, limit = taille_file-len(file))
        crawl(titles)
        deja_vu.append(titles)
        if file == []:
            file = no_links()
        titles = file
        file = []

    File_temp = session.query(File).all()
    print(File_temp)
    if File_temp != []:
        for fichier in File_temp:
            F = session.query(File).filter(fichier).first()
            session.delete(F)
            session.commit()
    for fichier in titles:
        F = File(titre=fichier)
        session.add(F)
        session.commit()
    print("end")


except Exception as exp:
    print(exp)