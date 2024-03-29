from django.db.models.query import QuerySet
from rich.console import Console
from rich.table import Table


class WordDisplay:
    def __init__(self, search_results):
        if isinstance(search_results, QuerySet):
            self.search_results = search_results
        else:
            self.search_results = [search_results]

    def display(self):
        if self.search_results == [None]:
            console = Console()
            return console.print("No results found.")

        table = Table(
            title=f"Results for look up: {self.search_results[0].lookup_word}"
        )

        table.add_column("looked up word", style="magenta")
        table.add_column("lemma", style="magenta")
        table.add_column("en", justify="left", style="green")
        table.add_column("definition", justify="left", style="cyan")
        table.add_column("examples", justify="left")
        for i in self.search_results:
            try:
                examples = ""
                if i.examples:
                    example_list = [f"{x['lang']}: {x['example']}" for x in i.examples]
                    examples = "\n".join(example_list)
            except KeyError:
                examples = ""

            table.add_row(
                i.lookup_word, i.lemma, i.en_translation, i.definition, examples
            )

        console = Console()
        return console.print(table, justify="center")
