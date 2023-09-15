from django.shortcuts import render
from .models import Word


def lemma_detail_view(request, lemma):
    objects = Word.objects.filter(lemma=lemma)
    context = {
        "lemma": lemma,
        "objects": objects,
    }
    return render(request, "lemma_detail.html", context)
