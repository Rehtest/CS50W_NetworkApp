import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post

POST_PER_PAGE = 10

def index(request):
    if request.method == "POST":
        user = request.user
        post = request.POST["post_text"]
        new_post = Post(user=user, post=post)
        new_post.save()
    
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, POST_PER_PAGE)

    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": all_posts,
        "some_posts": paginated_posts
        })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def user_page(request, user_view):
    # Get details of the user selected
    user_details = User.objects.get(username=user_view)
    user_id = User.objects.get(username=user_view).id
    user_posts = Post.objects.filter(user=user_id)

    # Add Pagination
    paginator = Paginator(user_posts, POST_PER_PAGE)

    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    # If follow button clicked in profile.html -> Add or remove current user to list of followers
    if request.method == "POST":
        follow_choice = request.POST["follow"]
        if follow_choice == "follow":
            user_details.followers.add(request.user)
        elif follow_choice == "unfollow":
            user_details.followers.remove(request.user)

    # Tag whether the follow button on the user's profile should be to follow / unfollow
    if request.user in user_details.followers.all():
        follow_button = "Unfollow"
    else:
        follow_button = "Follow"

    # Identify number of followers and following for the user
    user_followers_count = user_details.followers_count()
    user_following_count = user_details.following_count()      


    return render(request, "network/profile.html", {
        "user_details": user_details,
        "followers_count": user_followers_count,
        "following_count": user_following_count,
        "posts": paginated_posts,
        "follow_button": follow_button
    })

# Page for posts from those users that the current user is following
def following(request):
    current_user = request.user
    followed_users = User.objects.filter(followers=current_user)
    all_posts = Post.objects.filter(user__in=followed_users)

    # Add Pagination
    paginator = Paginator(all_posts, POST_PER_PAGE)

    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    #print(all_posts)
    return render(request, "network/following.html", {
        "posts": paginated_posts
    })

@csrf_exempt
@login_required
def save(request):
    
    # Saving a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Check if user is owner of the post
    data = json.loads(request.body)
    post_number = data["post_id"]
    post_data = data["content"]

    edit_post = Post.objects.get(id=post_number)
    if request.user == edit_post.user:
        print(data["content"])
        edit_post.post = post_data
        edit_post.edited = True
        edit_post.save()
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def like(request):

    # Liking a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "Post request required."}, status=400)

    # Add user to liked list
    data = json.loads(request.body)
    post_number = data["post_id"]
    like_status = data["like"]
    
    edit_post = Post.objects.get(id=post_number)
    if like_status == "like":
        edit_post.likes.add(request.user)
    elif like_status == "unlike":
        edit_post.likes.remove(request.user)
    edit_post.save()
    new_like_number = edit_post.likes.count()
    print(new_like_number)
    return JsonResponse({
        "like_count": new_like_number
    })
    