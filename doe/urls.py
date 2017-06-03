from django.conf.urls import url
from . import views
app_name = 'doe'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^exp1/', views.exp1, name='exp1')

]