from django.db import models

class Word(models.Model):
    
    SOURCE_LANGS = (
        ('en_us', 'English'),
        ('fr_fr', 'French'),
        ('it_it', 'Italian'),
        ('ka_ge', 'Georgian'),
        ('pl_pl', 'Polish'),
        ('se_se', 'Swedish'),
        ('zh_cn', 'Chinese (Mandarin)'),
    )


    TARGET_LANGS = (
        ('en_us', 'English'),
    )


    POS_CHOICES = (
        ('NOUN', 'Noun'),
        ('VERB', 'Verb'),
        ('ADJ', 'Adjective'),
        ('ADV', 'Adverb'),
        ('PRON', 'Pronoun'),
        ('PROPN', 'Proper Noun'),
        ('PREP', 'Preposition'),
        ('CONJ', 'Conjunction'),
        ('INTJ', 'Interjection'),
        ('DET', 'Determiner'),
        ('NUM', 'Numeral'),
        ('PART', 'Particle'),
        ('AUX', 'Auxiliary'),
        ('PHRASE', 'Phrase'),
        ('X', 'Other')
)

    source_lang = models.CharField("Source Language", max_length=6, choices=SOURCE_LANGS)
    target_lang = models.CharField("Target Language", max_length=6, choices=TARGET_LANGS)
    lookup_word = models.CharField("Lookup Word", max_length=50)
    lemma = models.CharField("Lemma", max_length=50)
    native_alpha_lemma = models.CharField("Native Alphabet Lemma", max_length=50)
    pos = models.CharField("Part of Speech", max_length=240, choices=POS_CHOICES)
    is_phrase = models.BooleanField("Is Phrase", default=False) # Non-char field
    definition = models.JSONField("Definition") # Non-char field
    definition_source = models.URLField("Definition Source") # Non-char field
    examples = models.JSONField("Examples") # Non-char field
    pos_forms = models.JSONField("Part of Speech Forms") # Non-char field
    date = models.DateField("Date added", auto_now_add=True) # Non-char field
    

    def __str__(self):
        return self.lemma