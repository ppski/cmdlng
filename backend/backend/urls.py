from django.contrib import admin
from django.urls import path, re_path
from words import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("lemma/<str:lemma>/", views.lemma_detail_view),
]
