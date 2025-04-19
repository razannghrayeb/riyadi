from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("news",views.news_All,name="news_All"),
   path("news/<int:id>",views.singleNews,name="singleNews"),
   path("OurTeam",views.OurTeam,name="OurTeam"),
   path("book_field/", views.list_fields, name="list_fields"),
   path('book/<int:field_id>/', views.book_field, name='book_field')
]