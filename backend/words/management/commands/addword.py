from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import Word
from ...lookup import WordLookUp, WordSearch


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-a", "--add", nargs=1, type=str, help="Add a new word")
        parser.add_argument("-sl", "--source_lang", type=str, help="Lang of input word")
        parser.add_argument(
            "-tl", "--target_lang", type=str, help="Lang of target word (translation)"
        )

    def handle(self, *args, **options):
        # Languages
        if options["source_lang"]:
            if isinstance(options["source_lang"], list):
                LANG_SOURCE = options["source_lang"][0]
            elif isinstance(options["source_lang"], str):
                LANG_SOURCE = options["source_lang"]
        else:
            LANG_SOURCE = settings.LANG_SOURCE

        if options["target_lang"]:
            if isinstance(options["target_lang"], list):
                LANG_TARGET = options["target_lang"][0]
            elif isinstance(options["target_lang"], str):
                LANG_TARGET = options["target_lang"]
        else:
            LANG_TARGET = settings.LANG_TARGET

        # Add word
        if options["add"]:
            lookup_word_str = options["add"][0].lower()
            search = WordSearch(
                lookup_word=lookup_word_str,
                lang_source=LANG_SOURCE,
                lang_target=LANG_TARGET,
            )
            db_search_result = search.search(lookup_word=lookup_word_str)

            if db_search_result:
                print("The word is already in the db: ", db_search_result)
            else:

                print(f"Searching for {lookup_word_str}...")
                lookup = WordLookUp(
                    lookup_word=lookup_word_str,
                    lemma=search.lemma,
                    lang_source=LANG_SOURCE,
                    lang_target=LANG_TARGET,
                )
                text = lookup.look_up()

                if not text:
                    print("No results found.")
                else:
                    print(text)
