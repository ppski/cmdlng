from django.db import models


class Word(models.Model):
    SOURCE_LANGS = (
        ("en_us", "English"),
        ("fr_fr", "French"),
        ("it_it", "Italian"),
        # ("ka_ge", "Georgian"),  # TODO
        ("pl_pl", "Polish"),
        ("se_se", "Swedish"),
        # ("zh_cn", "Chinese (Mandarin)"),  # TODO
    )

    TARGET_LANGS = (
        ("en_us", "English"),
        ("fr_fr", "French"),
    )

    POS_CHOICES = (
        ("NOUN", "Noun"),
        ("VERB", "Verb"),
        ("VPHRASE", "Verb Phrase"),
        ("ADJ", "Adjective"),
        ("ADV", "Adverb"),
        ("PRON", "Pronoun"),
        ("PROPN", "Proper Noun"),
        ("PREP", "Preposition"),
        ("CONJ", "Conjunction"),
        ("INTJ", "Interjection"),
        ("DET", "Determiner"),
        ("NUM", "Numeral"),
        ("PHRASE", "Phrase"),
        ("X", "Other"),
    )

    date = models.DateTimeField("Date added", auto_now_add=True)  # Non-char field
    lang_source = models.CharField(
        "Source Language", max_length=6, choices=SOURCE_LANGS
    )
    lang_target = models.CharField(
        "Target Language",
        max_length=6,
        choices=TARGET_LANGS,
        default="en_us",
        blank=False,
        null=False,
    )

    lookup_word = models.CharField("Lookup Word", max_length=75)
    lemma = models.CharField("Lemma", max_length=75)
    related_lemma = models.CharField(
        "Related Lemma", max_length=75, null=True
    )  # For related expressions

    native_alpha_lemma = models.CharField(
        "Native Alphabet Lemma", max_length=75, null=True
    )
    pos = models.CharField(
        "Part of Speech", max_length=10, choices=POS_CHOICES, null=True
    )
    en_translation = models.CharField("English Translation", max_length=75, null=True)
    definition = models.JSONField("Definition", null=True)  # Non-char field
    examples = models.JSONField("Examples", null=True)  # Non-char field
    pos_forms = models.JSONField("Part of Speech Forms", null=True)  # Non-char field
    is_mwe = models.BooleanField(
        "Is Multi-Word Expression", default=False
    )  # Non-char field
    is_informal = models.BooleanField("Informal", default=False)  # Non-char field
    source = models.URLField("Definition Source")  # Non-char field
    llm = models.CharField("LLM", max_length=25, null=True)  # Non-char field

    def __str__(self):
        return self.lemma
