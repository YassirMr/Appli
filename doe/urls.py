from django.conf.urls import url
from . import views
app_name = 'doe'

urlpatterns = [
    url(r'^$', views.Introduction, name='Introduction'),
    url(r'^exp1/', views.exp1, name='exp1'),
    url(r'^result1/', views.result1, name='result1'),
    url(r'^index/', views.index, name='index') #this is just the summary part
]