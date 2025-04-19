from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Game
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required(login_url='/auth/login/')
def home(request):
    games = Game.objects.all()
    return render(request, 'TicketShop.html', {'games': games})
@login_required(login_url='/auth/login')
def ticket_detail(request, ticket_id):
    ticket = Game.objects.get(id=ticket_id)
    user_has_ticket = ticket.is_user_attendee(request.user)
    amount_in_cents = int(ticket.price * 100)

    if request.method == 'POST' and not user_has_ticket:
        
        try:
            # Token is created using Checkout or Elements
            # Get the payment token ID submitted by the form:
            token = request.POST['stripeToken']
            charge = stripe.Charge.create(
                amount=int(ticket.price * 100),  # amount in cents
                currency='usd',
                description=f'Purchase of {ticket.name}',
                source=token,
            )
            ticket.tickets_sold += 1
            ticket.attendees.add(request.user)
            ticket.save()
            messages.success(request, "You have successfully purchased a ticket.")
            return render(request, 'TicketDetail.html', {
            'ticket': ticket, 
            'user_has_ticket': True, 
         
        })
        except stripe.error.StripeError as e:
            messages.error(request, "Payment error: " + str(e))
        except Exception as e:
            messages.error(request, "An error occurred, unable to complete the purchase.")

    return render(request, 'TicketDetail.html', {
            'ticket': ticket, 
            'user_has_ticket': user_has_ticket, 
            'amount_in_cents': amount_in_cents,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        })