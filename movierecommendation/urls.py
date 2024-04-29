from django.urls import re_path as url
from movierecommendation import views

urlpatterns = [
    url(r'^movie', views.doubanRecommendation, name='movieRecommendation'),
    url(r'^weibo', views.weiboRecommendation, name='weiboRecommendation'),

    url(r'^buildindex', views.buildindex, name='doubanIndex'),
    url(r'^searchindex', views.searchindex, name='searchIndex'),

    url(r'^wbbuildindex', views.weibobuildindex, name='weiboIndex'),
    url(r'^wbsearchindex', views.weiboSearchIndex),

    url(r'^posannotation', views.posannotation, name='posAnnotation')
]
