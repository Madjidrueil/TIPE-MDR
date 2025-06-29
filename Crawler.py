import requests
import os
import time
from extracts import *


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
            if type(page.get('extract')) == str :
                content = page.get('extract')
                valid_urls.append(title)
                save_to_file(title,content,directory)
            else:
                print(title)
        else:
            raise Exception(f"HTTP Error: {response.status_code}")
    return valid_urls



def save_to_file(title, content, directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Nettoyer le titre pour éviter les caractères interdits dans les noms de fichiers
    #l'ajouter dans le dictionnaire de conversion
    safe_title = title.replace("/", "_").replace("\\", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
    filename = os.path.join(directory, f"{safe_title}.txt")

    with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

directory = "extrait_1"
def crawl(titles):
    ti = time.time()
    print("Step 1")
    time.sleep(0.5)
    bdd = valid_url(titles)
    print("temp step 1 : " + str(time.time()-ti))
    print("end_scrapper")


