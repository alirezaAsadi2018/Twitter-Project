from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TweetForm, EditForm, EditUserNameForm
from .models import Tweet, Like, User, Follow, HashTag, Tag
import json
from rest_framework import generics
from .serializers import SearchTweetsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


def handle_uploaded_file(f, username):
    with open('static/userprofile/image/'+username+'.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def home(request):
    if request.method == 'GET':
        context = {}
        context['tweets'] = Tweet.objects.all().order_by('-create_datetime')
        context['likes'] = []
        if request.user.is_authenticated:
            context['likes'] = list(Like.objects.filter(user=request.user).values_list('tweet_id', flat=True))
        return render(request, 'userprofile/home.html', context)

def edit(request):
    if request.method == 'GET':
        form = EditForm(request.POST, request.FILES, instance=request.user, initial={'biography': request.user.biography})
    elif request.method == 'POST':
        form = EditForm(request.POST or None, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image']:
                request.user.image = form.cleaned_data['image']
            if form.cleaned_data['biography']:
                request.user.biography = form.cleaned_data['biography'] 
            request.user.save()
            return redirect('home')
    return render(request, 'userprofile/edit.html', {'form': form})


def usernameedit(request):
    if request.method == 'GET':
        form = EditUserNameForm()
    elif request.method == 'POST':
        form = EditUserNameForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['username']:
                request.user.username = form.cleaned_data['username']
                request.user.save()
                return redirect('home')
    return render(request, 'userprofile/edit.html', {'form': form})


def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return HttpResponseRedirect(request.GET.get('next', '/login/'))
        # else:
        #     messages.error(request, form.errors)
    return render(request, 'userprofile/signup.html', {'form': form})


def login_account(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                messages.error(request, u'Please enter a correct username and password.\r\n' + 
                    'Note that both fields may be case-sensitive.')
    return render(request, 'userprofile/login.html', {'form': form})


@login_required
def logout_account(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/login/'))


@login_required
def tweet(request):
    if request.method == 'GET':
        form = TweetForm()
    else:
        try:
            form = TweetForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data['text'] or form.cleaned_data['file']:
                    newTweet = Tweet()
                    newTweet.owner = request.user
                    newTweet.text = form.cleaned_data['text']
                    newTweet.file = form.cleaned_data['file']
                    newTweet.save()
                    return redirect('home')
                else:
                    messages.error(request, u' Tweet body text and file can\'t be empty at the same time!\n' + 
                        'Please provide one of them with data!')
            else:
                messages.error(error, u'Bad data passed in. Please try again.')
        except ValueError:
            messages.error(error, u'Bad data passed in. Please try again.')
    return render(request, "userprofile/tweetForm.html", {'form': form})


def interaction(request, special=False):
    if not request.user.is_authenticated:
        redirect('login')
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    if action == 'retweet':
        tweet = Tweet.objects.get(id=itemId)
        newTweet = Tweet()
        newTweet.owner = request.user
        newTweet.text = tweet.text
        newTweet.file = tweet.file
        main_tweet = tweet
        while main_tweet.retweet:
            main_tweet = main_tweet.retweet
        newTweet.retweet = main_tweet
        newTweet.save()
    elif action == 'like':
        tweet = Tweet.objects.get(id=itemId)
        newLike = Like()
        newLike.tweet = tweet
        newLike.user = request.user
        tweet.like_count += 1
        tweet.save()
        newLike.save()
    elif action == 'dislike':
        tweet = Tweet.objects.get(id=itemId)
        like = Like.objects.filter(tweet=tweet, user= request.user)
        like.delete()
        tweet.like_count -=1
        tweet.save()
    elif action == 'follow':
        selected_user = User.objects.get(id=itemId)
        follow = Follow()
        follow.follower = request.user
        follow.followed = selected_user
        follow.save()

    elif action == 'unfollow':
        selected_user = User.objects.get(id=itemId)
        following = Follow.objects.filter(followed=selected_user, follower=request.user)
        following.delete()

    elif action == "remove":
        tweet = Tweet.objects.get(id=itemId)
        tweet.delete()

    return JsonResponse('Item was added', safe=False)


def profile(request, selected_user_id):
    context = {}
    selected_user = get_object_or_404(User, pk=selected_user_id)
    context['selected_user'] = selected_user
    if request.user.is_authenticated:
        flag = Follow.objects.filter(followed=selected_user, follower=request.user)
        following = False
        if flag:
            following = True
        context['following'] = following
    context['likes'] = []
    context['tweets'] = Tweet.objects.filter(owner=selected_user).order_by('-create_datetime')
    if request.user.is_authenticated:
        context['likes'] = list(Like.objects.filter(user=request.user).values_list('tweet_id', flat=True))

    return render(request, 'userprofile/profile.html', context)


def likes(request, selected_tweet_id):
    context = {}
    selected_tweet = get_object_or_404(Tweet, pk=selected_tweet_id)
    context['likes'] = Like.objects.filter(tweet=selected_tweet)
    return render(request, 'userprofile/like.html', context)


class SearchTweetsApiView(APIView):
    queryset = Tweet.objects.all()
    serializer_class = SearchTweetsSerializer


    def get(self, request, *args, **kwargs):
        search_text = kwargs.get('search_text')
        result_tweet_ids = []
        if not search_text:
            return
        if search_text.startswith('@'):
            # search by username 
            users_list = list(User.objects.filter(username=search_text.strip("@")))
            result_tweet_ids = Tweet.objects.filter(owner__in=users_list).values_list('id', flat=True)
        elif search_text.startswith('*'):
            # search by hashtags
            result_hashtags_list = list(HashTag.objects.filter(tag=search_text.strip("*")))
            result_tweet_ids = Tag.objects.filter(hashtag__in=result_hashtags_list).values_list('tweet', flat=True)
        else:
            # search in tweet text
            result_tweet_ids = Tweet.objects.filter(text__contains=search_text).values_list('id', flat=True)
        return Response({
            'result': list(result_tweet_ids)
        })


@login_required()
def logs(request):
    context = {}
    context['likes'] = Like.objects.all().order_by('-like_datetime')
    context['follows'] = Follow.objects.all().order_by('-follow_datetime')
    context['retweets'] = Tweet.objects.all().order_by('-create_datetime')

    return render(request, 'userprofile/log.html', context)


def hashtag(request, tag):
    context = {}
    context['tweets'] = Tweet.objects.all().order_by('-create_datetime')
    context['likes'] = []
    if request.user.is_authenticated:
        context['likes'] = list(Like.objects.filter(user=request.user).values_list('tweet_id', flat=True))
    context['search_field'] = '#' + tag
    return render(request, 'userprofile/home.html', context)


