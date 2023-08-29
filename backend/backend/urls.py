from django.contrib import admin
from django.urls import path, re_path
from words import views


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api/words/$", views.words_list),
    re_path(r"^api/words/([0-9])$", views.words_detail),
]
