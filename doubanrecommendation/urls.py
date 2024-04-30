"""doubanrecommendation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from movierecommendation import views

urlpatterns = [
    url(r'^movie', include('movierecommendation.urls')),
    url(r'^weibo', include('movierecommendation.urls')),
    url(r'image', include('movierecommendation.urls')),

    url(r'^movie', views.doubanRecommendation),
    url(r'^weibo', views.weiboRecommendation),
    url(r'^image', views.doubanClassification),

    url(r'^buildindex', include('movierecommendation.urls')),

    url(r'^admin', admin.site.urls),
    url(r'^$', views.weiboRecommendation),

    url(r'^buildindex', views.buildindex),
    url(r'^searchindex', views.searchindex),
    url(r'^wbbuildindex', views.weibobuildindex),
    url(r'^wbbuildindex', include('movierecommendation.urls')),
    url(r'^wbsearchindex', views.weiboSearchIndex),
    url(r'^wbsearchindex', include('movierecommendation.urls')),

    url(r'^posannotation', views.posannotation),

    url(r'^nerannotation', views.nerannotation),
]
urlpatterns += staticfiles_urlpatterns()





