from django.core.management.base import BaseCommand
from django.conf import settings
from rich.console import Console
from ...lookup import WordLookUp, WordSearch
from ...display import WordDisplay


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-a", "--add", nargs=1, type=str, help="Add a new word")
        parser.add_argument(
            "-sl", "--source_lang", type=str, help="Lang of input word."
        )
        parser.add_argument(
            "-tl", "--target_lang", type=str, help="Lang of target word (translation)."
        )
        parser.add_argument(
            "-llm", "--llm", nargs="?", const="default", help="Use an LLM."
        )
        parser.add_argument(
            "-vw", "--view_word", nargs="?", type=str, help="View a word."
        )

    def handle(self, *args, **options):
        # Source lang
        if options["source_lang"]:
            if isinstance(options["source_lang"], list):
                LANG_SOURCE = options["source_lang"][0]
            elif isinstance(options["source_lang"], str):
                LANG_SOURCE = options["source_lang"]
        else:
            LANG_SOURCE = settings.LANG_SOURCE

        # Target lang
        if options["target_lang"]:
            if isinstance(options["target_lang"], list):
                LANG_TARGET = options["target_lang"][0]
            elif isinstance(options["target_lang"], str):
                LANG_TARGET = options["target_lang"]
        else:
            LANG_TARGET = settings.LANG_TARGET

        # LLM preference
        if options["llm"] is None:
            LLM = False
        elif options["llm"] == "default":
            LLM = settings.DEFAULT_LLM
        else:
            LLM = options["llm"]

        # Add word
        if options["add"]:
            lookup_word_str = options["add"][0].lower()
            search = WordSearch(
                lookup_word=lookup_word_str,
                lang_source=LANG_SOURCE,
                lang_target=LANG_TARGET,
            )
            db_search_result = search.search()

            if db_search_result:
                print("The word is already in the db: ", db_search_result)
            else:
                print(f"Searching for {lookup_word_str}...")
                lookup = WordLookUp(
                    lookup_word=lookup_word_str,
                    lemma=search.lemma,
                    lang_source=LANG_SOURCE,
                    lang_target=LANG_TARGET,
                    llm=LLM,
                )
                text = lookup.look_up()

                if not text:
                    print("No results found.")
                else:
                    print(text)

        elif options["view_word"]:
            lookup_word_str = options["view_word"].lower()
            search = WordSearch(lookup_word_str, LANG_SOURCE, LANG_TARGET)
            search_result = search.search()

            if search_result:
                display = WordDisplay(search_result)
                display.display()
            else:
                console = Console()
                console.print("No results.", style="bold red")
