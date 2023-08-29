from rest_framework import serializers
from .models import Word


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word

        fields = ('source_lang', 'target_lang', 'lookup_word', 'lemma', 'native_alpha_lemma', 'pos', 'is_phrase', 'definition', 'definition_source',  'examples', 'pos_forms', 'date')