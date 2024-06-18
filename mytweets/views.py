from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'index.html')

def tweet_list(request):
    tweets= Tweet.objects.all().order_by('-created_at')
    # orders the queryset (tweets) by the created_at field in descending order (- sign denotes descending order), so the most recent tweets appear first.
    return render(request,'tweet_list.html',{'tweets':tweets})

# The @login_required decorator in Django is used to restrict access to views that require authentication
@login_required
def tweet_create(request):
    if request.method=='POST':
        form=TweetForm(request.POST, request.FILES) #Accepts files in form as well
        if form.is_valid():
            tweet=form.save(commit=False) #does not save in models
            tweet.user=request.user 
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)      
    return render(request,'tweet_form.html',{'form':form})

# get_object_or_404() is a Django shortcut function that retrieves an object (Tweet in this case) from the database based on the given parameters (pk=tweet_id and user=request.user).

def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request,'tweet_confirm.html',{'tweet':tweet})

def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password()
    return render(request,'register/register.html',{'form':form})
