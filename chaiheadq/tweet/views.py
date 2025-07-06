from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegisterationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', { 'tweets' : tweets })

def search(request):
    print("GET data:", request.GET)
    query = request.GET.get('q')
    if query:
        tweets = Tweet.objects.filter(text__icontains=query)
    else:
        tweets = Tweet.objects.all()

    print("tweets:", tweets)
    return render(request, 'search.html', {'tweets': tweets})
     
        

@login_required # this is a decorator
def tweet_create(request):
    # three cases:
    # 1. its a post request then create the tweet
    # 2. its a get request then show the form
    if request.method == "POST": 
        # request.FILES means we are accepting/uploading a file
        # request.POST means we are accepting/uploading text
        form  = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=fasle means we don't want to save the form yet just keep it
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')  # go back to the tweet list.html
    else:
        # its fr get requst/ getting the form data
        form = TweetForm()
        return render(request, 'tweet_form.html', { 'form' : form })
    
    
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=id, user = request.user)
    if request.method == "POST":
        # we instance of the tweet , which s already in the databases
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            # commit=fasle means we don't want to save the form yet just keep it
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')  # go back to the tweet list.html
                
        else:
            form = TweetForm(instance=tweet)
            return render(request, 'tweet_form.html', { 'form' : form })    
        
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', { 'tweet' : tweet })
   
   
   
def register(request):
    if request.method == 'POST':
        form  =UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned_data means gives you the clean and safe values submitted in a form.
            user.set_password(form.cleaned_data['password1']) # take password and settin git
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegisterationForm()
        
    return render(request, 'registration/register.html', { 'form' : form })
    