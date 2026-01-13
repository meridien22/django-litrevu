from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from review.forms import TicketForm, ReviewForm
from review.models import Ticket, Review
from itertools import chain
from django.db.models import Q, Count, CharField, Value


# LoginRequiredMixin pour les classes correspond à  @login_required pour les fonctions
class Home(View):
    """Site homepage.

    Args:
        View : Base class for creating views.
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("flux")
        else:
            return redirect("login")


class Base(View):
    """Redirecting to the site's homepage.

    Args:
        View : Base class for creating views.
    """

    def get(self, request):
        return redirect("home")


@login_required
def posts(request):
    """Views presenting the user with their posts and allowing them to modify or delete them."""

    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    tickets = tickets.annotate(view=Value("POSTS", CharField()))
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(view=Value("POSTS", CharField()))

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    return render(request, "review/posts.html", context={"posts": tickets_and_reviews})


@login_required
def flux(request):
    """This view displays the user's own posts and those of the users they follow.
    It also allows the user to create a ticket or a review."""

    tickets = (
        Ticket.objects.filter(
            Q(user__followed_by__user=request.user) | Q(user=request.user)
        )
        .distinct()
        .annotate(nb_reviews=Count("review"))
    )

    # Plus performant et sans le distinct
    # user_ids = list(request.user.follows.values_list('id', flat=True))
    # user_ids.append(request.user.id)
    # tickets = Ticket.objects.filter(user_id__in=user_ids)

    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    reviews = (
        Review.objects.select_related("ticket")
        .filter(Q(user__followed_by__user=request.user) | Q(user=request.user))
        .distinct()
    )

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    return render(request, "review/flux.html", context={"posts": tickets_and_reviews})


@login_required
def ticket_create(request):
    """View allowing the creation of a ticket."""

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
    else:
        form = TicketForm()

    return render(request, "review/ticket_create.html", context={"form": form})


@login_required
def ticket_update(request, id):
    """View allowing modification of a ticket."""

    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = TicketForm(instance=ticket)

    return render(request, "review/ticket_update.html", context={"form": form})


@login_required
def ticket_review(request, id):
    """View allowing the creation of a review."""

    ticket = Ticket.objects.get(id=id)
    ticket.content_type = "TICKET"

    if request.method == "POST":
        form = ReviewForm(request.POST, prefix="review")
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("flux")
    else:
        form = ReviewForm(prefix="review")

    return render(
        request, "review/ticket_review.html", context={"ticket": ticket, "form": form}
    )


@login_required
def ticket_delete(request, id):
    """View allowing the deletion of a ticket."""

    ticket = Ticket.objects.get(id=id)
    ticket.content_type = "TICKET"

    if request.method == "POST":
        ticket.delete()
        return redirect("posts")

    return render(request, "review/ticket_delete.html", context={"ticket": ticket})


@login_required
def review_update(request, id):
    """View allowing the updating of a ticket."""

    review = Review.objects.get(id=id)
    ticket = review.ticket
    ticket.content_type = "TICKET"

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review, prefix="review")
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = ReviewForm(instance=review, prefix="review")

    return render(
        request, "review/review_update.html", context={"form": form, "ticket": ticket}
    )


@login_required
def review_delete(request, id):
    """View allowing the deletion of a review."""

    review = Review.objects.get(id=id)

    if request.method == "POST":
        review.delete()
        return redirect("posts")

    return render(request, "review/review_delete.html", context={"review": review})


@login_required
def ticket_review_create(request):
    """View allowing the creation of a ticket and a review."""

    if request.method == "POST":

        ticket_form = TicketForm(request.POST, request.FILES, prefix="ticket")
        review_form = ReviewForm(request.POST, prefix="review")

        if ticket_form.is_valid() and review_form.is_valid():

            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("flux")

    else:

        ticket_form = TicketForm(prefix="ticket")
        review_form = ReviewForm(prefix="review")

    return render(
        request,
        "review/ticket_review_create.html",
        context={"ticket_form": ticket_form, "review_form": review_form},
    )
