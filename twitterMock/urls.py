from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from stream_twitter import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twitterMock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', views.HomeView.as_view()),   
    url(r'^timeline/', login_required(views.TimelineView.as_view())),
    url(r'^user/(?P<user_name>.+)/$', views.user),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^discover/', login_required(views.discover)),
    url(r'^follow/$', login_required(views.follow), name='follow'),
    url(r'^unfollow/(?P<target_id>\d+)/$', login_required(views.unfollow), name='unfollow'),
    url(r'^hashtag/(?P<hashtag_name>.+)/', views.hashtag)
)
