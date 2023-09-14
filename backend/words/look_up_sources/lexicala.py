import requests

from django.conf import settings
from typing import Union

from ._diclookup import DictionaryLookUp


class Lexicala(DictionaryLookUp):
    @staticmethod
    def look_up(
        lookup_word: str,
        lemma: str,
        lang_prefix: str,
        lang_source: str,
        lang_target: str,
    ) -> Union[list, None]:
        response = requests.get(
            "https://lexicala1.p.rapidapi.com/search",
            headers={
                "X-RapidAPI-Key": settings.LEXICALA_API_KEY,
                "X-RapidAPI-Host": "lexicala1.p.rapidapi.com",
            },
            params={"text": lookup_word, "language": lang_prefix},
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
                    pos = Lexicala.clean_lookup_pos(result["headword"]["pos"])
                elif isinstance(result["headword"], list):
                    related_lemma = result["headword"][0]["text"]
                    pos = Lexicala.clean_lookup_pos(result["headword"][0]["pos"])

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
