from django.urls import path, re_path
from .views import (signup, home, login_account, logout_account, tweet, interaction, profile, likes, 
    SearchTweetsApiView, logs, edit, usernameedit, hashtag)

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_account, name='login'),
    path('tweet/', tweet, name='tweet'),
    path('likes<int:selected_tweet_id>/', likes, name='likes'),
    path('interaction/', interaction, name='interaction'),
    path('logout/', logout_account, name='logout'),
    path('logs/', logs, name='logs'),
    path('edit/', edit, name='edit'),
    path('usernameedit/', usernameedit, name='usernameedit'),
    path('profile<int:selected_user_id>/', profile, name='profile'),
    path('search/<str:search_text>/', SearchTweetsApiView.as_view(), name='search'),
    path('tags/<str:tag>/', hashtag, name='hashtag'),
]