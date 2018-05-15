from django.conf.urls import url
from . import views
from . import views as core_views

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^profile/(\d+)', views.profile, name='profile'),
    url(r'^new_post/', views.new_post, name='new_post'),
    url(r'^search/', views.search_profiles, name='search'),
    url(r'^comment/(\d+)', views.comment, name='comment'),
]
