from rich.console import Console
from rich.table import Table


class WordDisplay:
    def __init__(self, search_results):
        self.search_results = search_results

    def display(self):
        table = Table(title=f"Results for {self.search_results[0].lookup_word}")

        table.add_column("looked up word", style="cyan", no_wrap=True)
        table.add_column("lemma", style="magenta")
        table.add_column("en", justify="left", style="green")
        table.add_column("definition", justify="left", style="green")
        table.add_column("examples", justify="left", style="green")
        table.add_column("source", justify="left", style="green")
        for i in self.search_results:
            examples = ""
            try:
                if i.examples:
                    example_list = [f"{x['lang']}: {x['example']}" for x in i.examples]
                    examples = " | ".join(example_list)
            except KeyError:
                examples = ""

            source = (
                i.source.replace("www.", "")
                .replace("http://", "")
                .replace("https://", "")
            )
            table.add_row(
                i.lookup_word,
                i.lemma,
                i.en_translation,
                i.definition,
                examples,
                source,
            )

        console = Console()
        return console.print(table, justify="center")
