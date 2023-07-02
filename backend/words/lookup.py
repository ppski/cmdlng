
import requests
import json
import re

import spacy
from bs4 import BeautifulSoup

from .models import Word, Homonym, LookUp

from .api_keys import LEXICALA_API_KEY



class WordSearch:
    def __init__(self, lookup_word, lang_source="fr_fr", lang_target="fr_fr"):
        self.lookup_word = lookup_word
        self.lang_source = lang_source
        self.lang_target = lang_target


    def get_spacy_lemma(self):
        if self.lang_source == "fr_fr":
            nlp = spacy.load('fr_core_news_sm')
        elif self.lang_source == "en_us":
            nlp = spacy.load('en_core_web_sm')
        else:
            # Use EN for other languages
            nlp = spacy.load('en_core_web_sm')  

        doc = nlp(self.lookup_word)
        if len(doc) == 1:
            return doc[0].lemma_
        

    def search(self, lookup_word, lang_source="fr_fr", lang_target="fr_fr"):
        # Search for a word in the db

        # TODO: logic for MWEs
        # Look for word in db
        search_lookup_result = Word.objects.filter(lemma=lookup_word, lang_source=self.lang_source)

        if search_lookup_result:
            return search_lookup_result
        

        # Get lemma
        spacy_lemma = self.get_spacy_lemma()
        search_lemma_result = Word.objects.filter(lemma=spacy_lemma, lang_source=self.lang_source)
        if search_lemma_result:
            return search_lemma_result

        return None



class WordLookUp:
    def __init__(self, lookup_word, lang_source="fr_fr", lang_target="fr_fr", source="lexicala"):
        self.lookup_word = lookup_word
        self.lang_source = lang_source
        self.lang_target = lang_target
        self.lang_pair = f"{lang_source}-{lang_target}"
        self.source = self.get_search_pref()
        self.is_mwe = False
        self.is_informal = False
        
    def look_up(self):
        print("LOOK UP")
        results = self.get_search_pref()    
        for result in results:


            empty_dict = {
            "lang_source" : self.lang_source,
            "lang_target" : self.lang_target,
            "lookup_word" : self.lookup_word,
            "lemma" : result.get("lemma"),
            "native_alpha_lemma" : result.get("native_alpha_lemma"),
            "pos" : result.get("pow"),
            "is_mwe" :  self.is_mwe,
            "is_informal" :  self.is_informal,
            "en_translation" : result.get("en_translation"),
            "definition" : result.get("definition"),
            "source" : result.get("source"),
            "examples" : result.get("examples"),
            "pos_forms" : result.get("pos_forms"),}
            new_word = Word(**empty_dict)
    
            new_word.save()



    def clean_lookup_pos(self, lookup_pos):
        pos_dict = {'NOUN': ['noun', 'n'], 'VERB': ['verb', 'v'], 'ADJ': ['adjective'], 'ADV': ['adverb'], 'PRON': ['pronoun'], 'PROPN': ['proper noun'], 'PREP': ['preposition'], 'CONJ': ['conjunction'], 'INTJ': ['interjection'], 'DET': ['determiner'], 'NUM': ['numeral', 'number'], 'PHRASE': ['phrase'], 'X': ['other', 'unknown']}

        if lookup_pos.upper() in list(pos_dict.keys()):
            return lookup_pos.upper()
    
        lookup_pos = lookup_pos.strip((',', '.', ';', ':', '!', '?', ' ')).lower()
        # clean_string = re.sub(r'\W+', '', my_string)

        for pos in pos_dict:
            if lookup_pos in pos_dict[pos]:
                return lookup_pos.upper()
        # If no match
        return 'X'


    def get_search_pref(self):
        if self.lang_pair == "fr_fr-fr_fr":
            print('MATCH!')
            return self.look_up_lexicala()
        elif self.lang_pair == "it_it-en_us":
            return self.look_up_lexicala()


    def look_up_lexicala(self):

        url = "https://lexicala1.p.rapidapi.com/search"

        lang = self.lang_source[:2] # fr_fr -> fr

        querystring = {"text": self.lookup_word,"language": lang }

        headers = {
            "X-RapidAPI-Key": LEXICALA_API_KEY,
            "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)

        if response.json()['n_results'] == 0:
            #FIXME: handle
            print("No results")
            return None
        
        else:

            max_results = 3 if (n_results := response.json()['n_results']) >= 3 else n_results

            definitions = []
            for result in response.json()['results'][:max_results]:
                print(result)
                lemma = result['headword']['text']
                pos = self.clean_lookup_pos(result['headword']['pos'])
                definitions.append({"lemma": lemma, "pos": pos, "definition": result['senses'][0]["definition"],"source": "lexicala"})
            
            return definitions



l = WordLookUp("bébé", lang_source="fr_fr", lang_target="fr_fr")
print(l.lang_pair)
print(l.look_up())