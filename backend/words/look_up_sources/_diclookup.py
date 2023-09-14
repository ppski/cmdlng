from typing import Union


class DictionaryLookUp:
    def __init__(self):
        pass

    @classmethod
    def clean_lookup_pos(cls, lookup_pos: str) -> Union[str, None]:
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

    def look_up(
        self,
        lookup_word: str,
        lemma: str,
        lang_prefix: str,
        lang_source: str,
        lang_target: str,
    ) -> Union[list, None]:
        return [{"lemma": "lemma", "definitions": "definitions"}]
