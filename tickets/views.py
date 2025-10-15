from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from teams.models import Profile
from django.utils.decorators import method_decorator
from django.views import View
from .forms import StatusUpdateForm # Add StatusUpdateForm
from teams.decorators import developer_required, user_is_assigned_developer

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at') # Start with all tickets

    # Get the 'filter' query parameter from the URL
    filter_by = request.GET.get('filter')

    if filter_by == 'my_tickets':
        tickets = tickets.filter(assigned_to=request.user)
    elif filter_by in Ticket.Status.values:
        tickets = tickets.filter(status=filter_by)

    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
        'statuses': Ticket.Status.choices  # Pass statuses for the filter dropdown
    })

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.reported_by = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
@developer_required
@user_is_assigned_developer
def update_ticket_status(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=ticket.pk)
    # This view will only be rendered via POST from the detail page,
    # so a GET request handling is not strictly necessary but good practice.
    return redirect('ticket_detail', pk=ticket.pk)