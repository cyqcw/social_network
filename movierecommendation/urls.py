from django.urls import re_path as url
from movierecommendation import views

urlpatterns = [
    url(r'^movieRecommendation', views.doubanRecommendation, name='movieRecommendation'),
    url(r'^buildindex', views.buildindex, name='doubanIndex'),
    url(r'^searchindex', views.searchindex, name='searchIndex')
]
