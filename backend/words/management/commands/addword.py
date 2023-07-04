from django.core.management.base import BaseCommand, CommandError
from ...models import Word
from ...lookup import WordLookUp, WordSearch


LANG_SOURCE = "fr_fr"
LANG_TARGET = "fr_fr"


class Command(BaseCommand):
    help = "TODO"

    def add_arguments(self, parser):
        parser.add_argument("-a", "--add", nargs=1, type=str, help='Add a new word')
        parser.add_argument("-s", "--search", nargs=1, type=str, help='Search for a word in db')


    def handle(self, *args, **options):
        if options['add']:

            search = WordSearch(lookup_word=options['add'], lang_source=LANG_SOURCE, lang_target=LANG_TARGET)
            db_search_result = search.search(lookup_word=options['add'], lang_source=LANG_SOURCE, lang_target=LANG_TARGET)

            if db_search_result:
                # Display existing entries
                pass
            else:

                lookup = WordLookUp(lookup_word=options['add'], lang_source=LANG_SOURCE, lang_target=LANG_TARGET)
                new_entry = Word(lemma=options['add'], lang_source=LANG_SOURCE, lang_target=LANG_TARGET, is_mwe=False, is_informal=False)


                new_entry.save()
                
        
        elif options['view']:
            pass
        elif options['search']:
            pass

