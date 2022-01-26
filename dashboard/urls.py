import debug_toolbar
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('top10', views.top10, name='top10'),
    path('recommend', views.recommend, name='recommend'),
    path('__debug__/', include(debug_toolbar.urls)),
    ]