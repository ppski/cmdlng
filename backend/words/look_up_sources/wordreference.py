import re
import requests

from bs4 import BeautifulSoup
from typing import Union

from ._diclookup import DictionaryLookUp


class WordReference(DictionaryLookUp):
    @staticmethod
    def look_up(
        lookup_word: str,
        lemma: str,
        lang_prefix: str,
        lang_source: str,
        lang_target: str,
    ) -> Union[list, None]:
        url = f"https://www.wordreference.com/{lang_prefix}en/"
        link = f"{url}{lemma}"

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
                    examples.append({f"{lang_prefix}": ex.text.strip()})

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
