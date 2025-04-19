
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
import time
from django.core.serializers import serialize

from django.db.models import Count


# Create your views here.


@login_required(login_url="/auth/login/")
def Community_index(request):  


    return render(request,"Community/Main_Community.html")

"""
Here I am fetching the posts using an API to render the posts 20 at a time this method is used to not overflow the system.
This view will accept a request from the index page as the user hovers over to the end of the page so it loads the page with the posts to be rendered
"""

def posts(request):
    
     #Get start and end points                                     #This code is similar to the code I viewed in CS50
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
   
    data = list(
    Post.objects
    .select_related('owner')
    .annotate(number_of_likes=Count('like'))
    .values(
        'id',
        'image',
        'owner__username',
        'date_uploaded',
        'number_of_likes',
        'caption',
        "owner__image"
    )[start:end+1]
    )


    #Artificially delay speed of response
    #time.sleep(1)

    # Return list of posts
    return JsonResponse({
        "posts": data
    },safe=False)


def has_liked_post(request, post_id):
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(user=request.user, post_id=post_id).exists()
        return JsonResponse({'has_liked': user_has_liked})
    else:
        return JsonResponse({'has_liked': False})
    
def toggle_like(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            post = Post.objects.get(pk=post_id)
            user = request.user
            if Like.objects.filter(user=user, post=post).exists():
                Like.objects.filter(user=user, post=post).delete()
                liked = False
            else:
                Like.objects.create(user=user, post=post)
                liked = True
            return JsonResponse({'success': True, 'liked': liked})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Unauthorized or invalid request method'})
    

@login_required(login_url="/auth/login/")
def add_post(request):

    if request.method=="GET":
        return render(request,"Community/add_post.html")
        
        
    username = request.user
    caption = request.POST["caption"]
    image = request.POST["image"]
    
    post = Post(owner=username,caption=caption, image=image)
    post.save()

    return HttpResponseRedirect(reverse("Community_index"))