from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
import requests
import time
import re
from models import *
from extracts import *

#--------------------------------------------------------------------------------------
#                             ---Fonctions---


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
                temp_dict[word] += 1
        for word in temp_dict:
            W = Index_inverse(word_id = word, document = title, word_freq = temp_dict[word])
            session.add(W)
        session.commit()


def crawl(titles):
    ti = time.time()
    print("Step 1")
    time.sleep(0.5)
    bdd = valid_url(titles)
    print("temp step 1 : " + str(time.time() - ti))
    print("end_scrapper")
#--------------------------------------------------------------------------------------
#                           ---Code---

useless_words = ["le", "de", "un", "être", "et", "il",
                 "avoir", "ne", "je", "son", "la",
                 "que", "se", "qui", "ce", "dans", "en",
                 "du", "elle", "au", "pour", "par"]

db_url = 'sqlite:///bdd.db'
engine = create_engine(db_url)
try:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    titles = ext_1 + ext_2 + ext_3 + ext_4 + ext_5 + ext_6 + ext_7 + ext_8
    crawl(titles)



except Exception as exp:
    print(exp)