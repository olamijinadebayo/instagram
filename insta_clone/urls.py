from django.conf.urls import url
from . import views
from . import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^profile/(\d+)/$', views.profile, name='profile'),
    url(r'^new_post/', views.new_post, name='new_post'),
    url(r'^search/', views.search_profiles, name='search'),
    url(r'^comment/(\d+)', views.comment, name='comment'),
    url(r'^detail/(\d+)', views.detail, name='detail'),
    url(r'^likes/(\d+)', views.like_post, name="like_post"),
    url(r'^follow/(\d+)', views.follow, name="follow"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
