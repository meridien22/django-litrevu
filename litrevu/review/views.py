from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from review.forms import TicketForm
from review.models import Ticket

# LoginRequiredMixin pour les classes correspond à 
# @login_required pour les fonctions
class Home(View):
     def get(self, request):
        if request.user.is_authenticated:
           return redirect("posts") 
        else:
           return render(request, "review/home.html")

class Base(View):
     def get(self, request):
        return redirect("home")

@login_required
def posts(request):
   tickets = Ticket.objects.filter(user=request.user)
   return render(request,
            "review/posts.html",
            context={"tickets": tickets})

@login_required
def ticket_create(request):
   if request.method == 'POST':
      form = TicketForm(request.POST, request.FILES)
      if form.is_valid():
         ticket = form.save(commit=False)
         ticket.user = request.user
         ticket.save()
         return redirect("home")
   else:
      form = TicketForm()

   return render(request, "review/ticket_create.html", context={'form': form})



@login_required
def ticket_update(request, id):
   ticket = Ticket.objects.get(id=id)

   if request.method == 'POST':
      form = TicketForm(request.POST, instance=ticket)
      if form.is_valid():
         form.save()
         return redirect("posts") 
   else:
      form = TicketForm(instance=ticket)

   for field in form:
      print(field)
   
   return render(request,
                 "review/ticket_update.html",
                 context={"form": form})
