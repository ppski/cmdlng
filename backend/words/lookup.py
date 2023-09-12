import json
import re
import requests
from typing import Union

import spacy
from django.conf import settings
from bs4 import BeautifulSoup


from .models import Word


# Look for word in db
class WordSearch:
    def __init__(
        self,
        lookup_word: str,
        lang_source: str = settings.LANG_SOURCE,
        lang_target: str = settings.LANG_TARGET,
    ):
        self.lookup_word = lookup_word
        self.lang_source = lang_source
        self.lang_target = lang_target
        self.lemma = self.get_spacy_lemma()

    def get_spacy_lemma(self):
        if self.lang_source == "fr_fr":
            nlp = spacy.load("fr_core_news_sm")
        elif self.lang_source == "en_us":
            nlp = spacy.load("en_core_web_sm")
        else:
            # Use EN for other languages
            nlp = spacy.load("en_core_web_sm")

        doc = nlp(self.lookup_word)
        return doc[0].lemma_  # FIXME: MWEs

    def search(self) -> Union[Word, None]:
        # Search for a word in the db
        search_lookup_as_lemma_result = Word.objects.filter(
            lemma=self.lookup_word, lang_source=self.lang_source
        )

        if search_lookup_as_lemma_result:
            return search_lookup_as_lemma_result

        search_lookup_result = Word.objects.filter(
            lookup_word=self.lookup_word, lang_source=self.lang_source
        )
        if search_lookup_result:
            return search_lookup_result

        # Get lemma
        spacy_lemma = self.get_spacy_lemma()
        search_lemma_result = Word.objects.filter(
            lemma=spacy_lemma, lang_source=self.lang_source
        )
        if search_lemma_result:
            return search_lemma_result

        return None


# Look up word in APIs
class WordLookUp:
    def __init__(
        self,
        lookup_word: str,
        lemma: str,
        lang_source: str = "fr_fr",
        lang_target: str = "fr_fr",
        llm: Union[bool, str] = False,
    ):
        self.lookup_word = lookup_word
        self.lang_source = lang_source
        self.lang_prefix = lang_source[:2]  # fr_fr -> fr
        self.lang_target = lang_target
        self.lang_pair = f"{lang_source}-{lang_target}"
        self.lemma = lemma
        self.llm = llm

    def look_up(self) -> Union[str, None]:
        results = self.get_search_pref()

        if not results:
            return None

        for result in results:
            empty_dict = {
                "lang_source": self.lang_source,
                "lang_target": self.lang_target,
                "lookup_word": self.lookup_word,
                "lemma": self.lemma,  # This is the spacy lemma
                "related_lemma": result.get("related_lemma"),
                "native_alpha_lemma": result.get("native_alpha_lemma"),
                "pos": self.clean_lookup_pos(result.get("pos")),
                "en_translation": result.get("en_translation"),
                "definition": result.get("definition"),
                "source": result.get("source"),
                "examples": result.get("examples"),
                "pos_forms": result.get("pos_forms"),
                "is_mwe": False,  # FIXME
                "is_informal": False,  # FIXME
            }
            new_word = Word(**empty_dict)
            new_word.save()

        new_entry = Word.objects.filter(
            lemma=self.lemma, lang_source=self.lang_source
        ).first()
        return f"Added {self.lemma}: {new_entry}"

    def clean_lookup_pos(self, lookup_pos: str) -> Union[str, None]:
        if not lookup_pos:
            return None
        pos_dict = {
            "NOUN": ["noun", "n", "nm"],
            "VERB": ["verb", "v", "vtr", "vi", "vimp", "vimpers", "vrefl", "vimpv"],
            "VPHRASE": ["v expr", "v expression"],
            "ADJ": ["adjective"],
            "ADV": ["adverb"],
            "PRON": ["pronoun"],
            "PROPN": ["proper noun"],
            "PREP": ["preposition"],
            "CONJ": ["conjunction"],
            "INTJ": ["interjection", "interj", "inter"],
            "DET": ["determiner"],
            "NUM": ["numeral", "number"],
            "PHRASE": ["phrase"],
            "X": ["other", "unknown"],
        }

        if lookup_pos.upper() in list(pos_dict.keys()):
            return lookup_pos.upper()

        for pos in pos_dict:
            if lookup_pos in pos_dict[pos]:
                return pos
        # If no match
        return "X"

    def get_search_pref(self) -> Union[list, None]:
        preferred_results = None

        if self.llm and self.llm == "chatgpt":
            preferred_results = self.look_up_openai()
        elif self.lang_pair == "fr_fr-fr_fr":
            preferred_results = self.look_up_lexicala()
        elif self.lang_pair == "fr_fr-en_us":
            preferred_results = self.look_up_lexicala()
        elif self.lang_pair == "it_it-en_us":
            preferred_results = self.look_up_lexicala()
        if not preferred_results:
            return self.look_up_wordreference()
        return preferred_results

    # ------------------------------------------------------------ #
    # WORDREFERENCE API
    # ------------------------------------------------------------ #
    def look_up_wordreference(self) -> Union[list, None]:
        url = f"https://www.wordreference.com/{self.lang_prefix}en/"
        link = f"{url}{self.lemma}"

        response = requests.get(link)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        # Entries
        find_def = soup.find("div", {"id": "articleWRD"})
        html_text = find_def.prettify()

        html_text = re.sub(r"\s+", " ", html_text.replace("\n", " ").strip())
        entries = re.split(r"id=\"\w{4}\:\d+\">", html_text)

        definitions = []
        for entry in entries:
            entry_soup = BeautifulSoup(entry, "html.parser")

            # Related lemma
            related_lemma = entry_soup.find("td", {"class": "FrWrd"})
            if related_lemma:
                related_lemma = related_lemma.text.strip()
                related_lemma = re.sub(
                    r"(\s+(a|adj|adv|agg|avv|expr|invar|loc|n|nf|nm|pron|v|vi|vtr|\+),?)+$",
                    "",
                    related_lemma,
                ).strip()

            # EN
            trans_en = entry_soup.find("td", {"class": "ToWrd"})
            if trans_en:
                trans_en = trans_en.text.strip()
                trans_en = trans_en.split("⇒")[0].strip()
                trans_en = re.sub(
                    r"(\s+(a|adj|adv|agg|avv|expr|invar|loc|n|nf|nm|pron|v|vi|vtr|\+),?)+$",
                    "",
                    trans_en,
                )

                if trans_en.lower() in [
                    "anglais",
                    "français",
                    "inglese",
                    "italiano",
                    "english",
                    "french",
                    "italian",
                ]:
                    continue  # Ignore these entries

            # POS
            pos_source = entry_soup.find("em", {"class": "POS2"})
            if pos_source:
                pos_source = pos_source.text.strip()

            # Examples
            examples = []
            ex_source = entry_soup.find("td", {"class": "FrEx"}) or []
            for ex in ex_source:
                if ex and ex.text.strip() != "":
                    examples.append({f"{self.lang_prefix}": ex.text.strip()})

            ex_en = entry_soup.find("td", {"class": "ToEx"}) or []
            for en in ex_en:
                if en and en.text.strip() != "":
                    examples.append({"en": en.text.strip()})

            if not related_lemma and not pos_source and not examples and not trans_en:
                continue  # ignore if empty

            match = None
            for d in definitions:
                if d["en_translation"] == trans_en:
                    match = True
            if not match:
                definitions.append(
                    {
                        "related_lemma": related_lemma,
                        "pos": pos_source,
                        # "definition": None,
                        "source": "http://wordreference.com",
                        "examples": examples,
                        "en_translation": trans_en,
                    }
                )
        return definitions

    # ------------------------------------------------------------ #
    #  LEXICALA API
    # ------------------------------------------------------------ #
    def look_up_lexicala(self) -> Union[list, None]:
        response = requests.get(
            "https://lexicala1.p.rapidapi.com/search",
            headers={
                "X-RapidAPI-Key": settings.LEXICALA_API_KEY,
                "X-RapidAPI-Host": "lexicala1.p.rapidapi.com",
            },
            params={"text": self.lookup_word, "language": self.lang_prefix},
        )
        if response.status_code != 200:
            return None

        elif int(response.json()["n_results"]) == 0:
            return None
        else:
            max_results = (
                3 if (n_results := response.json()["n_results"]) >= 3 else n_results
            )

            definitions = []

            if not response.json()["results"]:
                return None
            for result in response.json()["results"][:max_results]:
                if isinstance(result["headword"], dict):
                    related_lemma = result["headword"]["text"]
                    pos = self.clean_lookup_pos(result["headword"]["pos"])
                elif isinstance(result["headword"], list):
                    related_lemma = result["headword"][0]["text"]
                    pos = self.clean_lookup_pos(result["headword"][0]["pos"])

                senses = [r for r in result["senses"] if "definition" in r]
                def_ = "; ".join(
                    [
                        s.get("definition")
                        for s in senses
                        if s.get("definition") not in ["", " "]
                    ]
                )
                if not def_ and not pos and not related_lemma:
                    continue  # ignore if empty

                definitions.append(
                    {
                        "related_lemma": related_lemma,
                        "pos": pos,
                        "definition": def_,
                        "source": "http://lexicala.com/",
                    }
                )

            return definitions

    # ------------------------------------------------------------ #
    # OPENAI LLM API
    # ------------------------------------------------------------ #
    def look_up_openai(self) -> Union[list, None]:
        import openai

        def get_word_info(
            definition: str,
            en_translation: str,
            examples: list,
            is_informal: bool,
            is_mwe: bool,
            lemma: str,
            pos: str,
            source: str,
        ):
            """Get word info."""
            word_info = {
                "pos": pos,
                "en_translation": en_translation,
                "is_informal": is_informal,
                "lemma": lemma,
                "definition": definition,
                "examples": examples,
                "is_mwe": is_mwe,
                "source": source,
            }

            return json.dumps(word_info)

        function_descriptions = [
            {
                "name": "get_word_info",
                "description": "Get word info.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "definition": {
                            "type": "string",
                            "description": "Definition of the word.",
                        },
                        "en_translation": {
                            "type": "string",
                            "description": "The translation into English.",
                        },
                        "examples": {
                            "type": "array",
                            "description": "Examples of the word in use.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "lang": {"type": "string"},
                                    "example": {"type": "string"},
                                },
                            },
                        },
                        "is_informal": {
                            "type": "boolean",
                            "description": "Whether or not the word is informal.",
                        },
                        "is_mwe": {
                            "type": "boolean",
                            "description": "Whether or not the word is a multi-word expression.",
                        },
                        "lemma": {
                            "type": "string",
                            "description": "Lemma",
                        },
                        "pos": {
                            "type": "string",
                            "description": "The part of speech.",
                        },
                        "source": {
                            "type": "string",
                            "description": "The URL source of the definition.",
                        },
                    },
                    "required": [
                        "definition",
                        "en_translation",
                        "examples",
                        "is_informal",
                        "is_mwe",
                        "lemma",
                        "pos",
                        "source",
                    ],
                },
            }
        ]

        user_prompt = f"""
        Lang source: {self.lang_source}
        Target language: {self.lang_target}
        Define the word {self.lookup_word} in {self.lang_target}.
        """

        openai.api_key = settings.OPENAI_API_KEY
        try:
            completion = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                temperature=0.0,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a multi-lingual dictionary.",
                    },
                    {"role": "user", "content": user_prompt},
                ],
                # Add function calling
                functions=function_descriptions,
                function_call="auto",
            )
        except openai.error.APIError as e:
            print(f"OpenAI error: {e}")
            return None

        output = completion.choices[0].message
        params = json.loads(output.function_call.arguments)

        return [params]
