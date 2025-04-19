from django.urls import path

from . import views

urlpatterns = [
   path("",views.Community_index,name="Community_index"),
   path("posts",views.posts, name="posts"),#API
   path('has_liked_post/<int:post_id>/', views.has_liked_post, name='has_liked_post'),#API
   path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'), #AJAX API
   path('add_new_post/',views.add_post, name="add_post"),
]