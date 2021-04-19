from django.contrib import admin
from .models import User, Tweet, Follow, Like, HashTag, Tag


admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(HashTag)
admin.site.register(Tag)
