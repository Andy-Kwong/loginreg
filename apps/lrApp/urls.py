from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'lr_index'),
    url(r'^create$', views.create, name = 'lr_create'),
    url(r'^success$', views.success, name = 'lr_success'),
    url(r'^login$', views.login, name = 'lr_login'),
    url(r'^logout$', views.logout, name = 'lr_logout')
]
