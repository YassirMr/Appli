from django.conf.urls import url
from heatmap import views
app_name = 'heatmap'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^import/', views.importer , name='importer'),
    url(r'^show/', views.show , name='show'),
    url(r'^node/', views.node , name='node'),
    url(r'^fit/', views.fit , name='fit'),
    url(r'^forfit/', views.forfit , name='forfit')

]