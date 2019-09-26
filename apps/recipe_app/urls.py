from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^register$',views.register),
    url(r'^welcome$',views.home),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^browse/(?P<cuisine>\w+)$', views.browse),
    url(r'^recipe/view/(?P<id>\d+)$',views.showrecipe),
    url(r'^search$',views.search),
    url(r'^surprise$',views.surprise),
    url(r'^like$',views.addtoFavorite),
    url(r'^profile$',views.profile),
    url(r'^removefav/(?P<id>\d+)$',views.removefav),
    url(r'^removeRecipe/(?P<id>\d+)$',views.removeRecipe),
    url(r'^add$',views.add),
    url(r'^editfav/(?P<id>\d+)$',views.editfav),
    url(r'new$',views.new)
]