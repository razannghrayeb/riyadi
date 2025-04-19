
from .models import *
from .util import *
from TicketShop.models import Game
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.


def index(request):

    recent_games = Game.objects.all().order_by("-date")[:5]  # Get the 5 most recent games
    
    return render(request,"Main/index.html",{
        "News": getNews(),
        "user":request.user,
        "games": recent_games
    })

def singleNews(request, id):

    singleNews = models.News.objects.get(id=id)

    return render(request,"Main/singleNews.html",{
        "News":singleNews
    })


def news_All(request):
    news = models.News.objects.all()
    return render(request, "Main/All_news.html",{
        "News": news
    })

def OurTeam(request):

    GK = Player.objects.filter(role="GoalKeeper")
    DF = Player.objects.filter(role="Defense")
    MD = Player.objects.filter(role="MiddleFeild")
    FR = Player.objects.filter(role="Forward")
    TR = Player.objects.filter(role="Trainer")

    return render(request, "Main/OurTeam.html", {
        "GK": GK,
        "DF": DF,
        "MD": MD,
        "FR": FR,
        "TR": TR
    })

def list_fields(request):
    fields = Field.objects.all()
    return render(request, 'Main/list_fields.html', {'fields': fields})

@login_required(login_url='/auth/login/')
def book_field(request, field_id):
    
    field = Field.objects.get(id=field_id)
    books = Booking.objects.filter(field=field)
    if request.method == 'POST':
        date = request.POST['date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
        existing_bookings = Booking.objects.filter(
            field=field,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
            
        if not existing_bookings.exists() and datetime.date.fromisoformat(date) >= datetime.date.today():
            new_booking = Booking(user=request.user, field=field, date=date, start_time=start_time, end_time=end_time)               
            new_booking.save()
        else:
            message = 'Your booking conflicts with an existing booking and has been cancelled.'
            return render(request, 'Main/booking_error.html', {'error_message': message, 'field': field})
            
        
            
        return redirect('list_fields')
        

    return render(request, 'Main/book_field.html', {'field': field,
                                                    'books': books})