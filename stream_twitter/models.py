from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from stream_django import activity
from stream_django.feed_manager import feed_manager

# Create your models here.
class Tweet(activity.Activity, models.Model):
    user = models.ForeignKey('auth.User')
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def print_self(self):
        print(self.text)

    @property
    def activity_object_attr(self):
        return self

    def parse_all(self):
        parts = self.text.split()
        hashtag_counter = 0
        mention_counter = 0
        result = {"parsed_text": "", "hashtags": [], "mentions": []}
        for index, value in enumerate(parts):
            if value.startswith("#"):
                parts[index] = "{hashtag" + str(hashtag_counter) + "}"
                hashtag_counter += 1
                result[u'hashtags'].append(slugify(value))
            if value.startswith("@"):
                parts[index] = "{mention" + str(mention_counter) + "}"
                mention_counter += 1
                result[u'mentions'].append(slugify(value))
        result[u'parsed_text'] = " ".join(parts)
        return result

class Follow(models.Model):
    user = models.ForeignKey('auth.User', related_name='friends')
    target = models.ForeignKey('auth.User', related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField()
    picture = models.ImageField(upload_to='profile_pictures', blank=True)
