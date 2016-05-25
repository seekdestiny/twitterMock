#django built-in library
from django.views.generic.edit import CreateView
from django.shortcuts import render_to_response, render, get_object_or_404,\
    redirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login as auth_login

#my own model and settings
from stream_twitter.models import Follow
from stream_twitter.models import Tweet
from django.contrib.auth.models import User
from twitterMock import settings

#third-party api
from stream_django.feed_manager import feed_manager
from stream_django.enrich import Enrich


enricher = Enrich()


# Create your views here.
class TimelineView(CreateView):
    model = Tweet
    fields = ['text']
    success_url = "/timeline/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TimelineView, self).form_valid(form)

    def get(self, request):
        feeds = feed_manager.get_news_feeds(request.user.id)
        activities = feeds.get('flat').get()['results']
        activities = enricher.enrich_activities(activities)
        #hashtags = Hashtag.objects.order_by('-occurrences')
        context = {
            'activities': activities,
            'form': self.get_form_class(),
            'login_user': request.user,
            #'hashtags': hashtags
        }
        return render(request, 'stream_twitter/timeline.html', context)

class HomeView(CreateView):
    greeting = "Welcome to Mini Twitter"

    def get(self, request):
        if not request.user.is_authenticated() and not settings.USE_AUTH:
            admin_user = authenticate(
                username=settings.DEMO_USERNAME, password=settings.DEMO_PASSWORD)
            auth_login(request, admin_user)
        context = RequestContext(request)
        context_dict = {
            'greeting': self.greeting,
            'login_user': request.user,
            'users': User.objects.order_by('date_joined')[:50]
        }
        return render_to_response('stream_twitter/home.html', context_dict, context)

def user(request, user_name):
    user = get_object_or_404(User, username=user_name)
    feeds = feed_manager.get_user_feed(user.id)
    activities = feeds.get()['results']
    activities = enricher.enrich_activities(activities)
    context = {
        'activities': activities,
        'user': user,
        'login_user': request.user
    }
    return render(request, 'stream_twitter/user.html', context)
