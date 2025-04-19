from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
import cloudinary.uploader
from . import util
from .models import User
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "authentication/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        country = request.POST["country"]



        if(not util.check_if_country_valid(country)):
            return render(request, "authentication/signup.html", {
                "message": "Please enter a Country"
            })
               

        # Ensure password matches confirmation
        password = request.POST["password"]

        if(not util.is_strong_password(password)):
            return render(request, "authentication/signup.html", {
                "message": "Password Must be atleast 8 characters long containing atleast one digit, one upercase letter, and one special character"
            })

        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "authentication/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,country=country)
            user.save()
        except IntegrityError:
            return render(request, "authentication/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "authentication/signup.html")


@login_required(login_url="/auth/login/")
def profile_view(request, id):

    if int(request.user.id) != int(id):
        print(request.user.id, id)
        return HttpResponseForbidden("You are not authorized to perform this action.")

    user = User.objects.get(id=id)  # Assuming a user exists with this username
    if request.method == "POST":
        # Update user information
        
        user.username = request.POST.get("username", "")
        user.email = request.POST.get("email", "")
        
        # Handle image upload
        image = request.FILES.get("image")
        if image:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(image)
            user.image = upload_result['url']  # Assuming you have a profile model related to your User model

        user.save()

        return render(request, "authentication/profile.html", {
            "message": "Profile updated successfully."
        })
    
    else:
            return render(request, "authentication/profile.html", {
            "message": "You have no permission to update this profile!"
        })
        
    # For GET requests
    return render(request, "authentication/profile.html")


