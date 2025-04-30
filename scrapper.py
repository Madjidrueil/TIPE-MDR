import requests
import os

def get_wikipedia_page(title, language='fr'):
    """
    Récupère une page Wikipedia via son API.
    :param title: Titre de la page Wikipedia (ex: 'Python (programming language)')
    :param language: Langue de Wikipedia (par défaut 'en')
    :return: Contenu brut de la page.
    """
    url = f"https://fr.wikipedia.org/w/api.php"

    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'explaintext': True,
        'titles': title
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        pages = data['query']['pages']
        page = next(iter(pages.values()))
        return page.get('extract', 'No extract found.')
    else:
        raise Exception(f"HTTP Error: {response.status_code}")

def save_to_file(title, content, directory="output"):
    """
    Sauvegarde le contenu dans un fichier texte dans un sous-dossier.
    :param title: Titre de la page (utilisé pour le nom de fichier)
    :param content: Contenu à sauvegarder
    :param directory: Nom du dossier de sortie
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Nettoyer le titre pour éviter les caractères interdits dans les noms de fichiers
    safe_title = title.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
    filename = os.path.join(directory, f"{safe_title}.txt")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    # Exemple d'utilisation :
    titles = [
    "Acropole d'Athènes"
] #PS : voir scrappé.py (j'ai pas fais de lien entre ces fichiers

    i = 0
    for title in titles:
        i+= 1
        print(str(i/5) + "%")
        #print(f"--- {title} ---")
        content = get_wikipedia_page(title)
        #print(content[:500])  # Affiche les 500 premiers caractères
        #print("\n\n")
        save_to_file(title, content)
