from django.conf.urls import url
from . import views
from . import views as core_views

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^profile/(\d+)', views.profile, name='profile'),
]
