from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from stream_twitter import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twitterMock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomeView.as_view()),   
    url(r'^timeline/', login_required(views.TimelineView.as_view())),
    url(r'^user/(?P<user_name>.+)/$', views.user),
)
