from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EventForm, TimeOptionFormSet
from .models import Event, TimeOption

class EventCreateView(LoginRequiredMixin, View):
    def get(self, request):
        event_form = EventForm(user=request.user)
        formset = TimeOptionFormSet(queryset=TimeOption.objects.none())
        return render(request, 'eventpoll/create_event.html', {
            'event_form': event_form,
            'formset': formset
        })

    def post(self, request):
        event_form = EventForm(request.POST, user=request.user)
        formset = TimeOptionFormSet(request.POST)

        if event_form.is_valid() and formset.is_valid():
            # Save event first, link creator properly
            event = event_form.save(commit=False)
            event.creator = request.user
            event.save()
            event_form.save_m2m()  # For visible_to many-to-many

            # Save all time options and assign to event
            time_options = formset.save(commit=False)
            for time_option in time_options:
                time_option.event = event
                time_option.save()

            return redirect('event_detail', event_id=event.id)  # Ensure event_detail view exists
        else:
            return render(request, 'eventpoll/create_event.html', {
                'event_form': event_form,
                'formset': formset
            })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Fetch all time options for this event
    time_options = event.time_options.all()

    # Fetch votes by the current user for this event's options
    user_votes = Vote.objects.filter(user=request.user, time_option__event=event).values_list('time_option_id', flat=True)

    if request.method == 'POST':
        # Process voting: user selects multiple time options
        selected_option_ids = request.POST.getlist('time_options')  # name attribute in form inputs must match

        # Remove old votes for this user/event
        Vote.objects.filter(user=request.user, time_option__event=event).delete()

        # Save new votes
        for option_id in selected_option_ids:
            option = TimeOption.objects.get(id=option_id)
            Vote.objects.create(user=request.user, time_option=option)

        return redirect('event_detail', event_id=event.id)

    return render(request, 'eventpoll/event_detail.html', {
        'event': event,
        'time_options': time_options,
        'user_votes': user_votes,
    })

class EventDetailView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)

        if not event.visible_to.filter(id__in=request.user.groups.all()).exists():
            return render(request, 'events/not_allowed.html')

        user_votes = Vote.objects.filter(user=request.user, time_option__event=event).values_list('time_option_id', flat=True)

        return render(request, 'events/event_detail.html', {
            'event': event,
            'user_votes': user_votes,
            'time_options': event.timeoption_set.all()
        })


    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)

        # Remove existing votes by this user for this event
        Vote.objects.filter(user=request.user, time_option__event=event).delete()

        selected_option_ids = request.POST.getlist('time_options')
        for option_id in selected_option_ids:
            time_option = TimeOption.objects.get(id=option_id)
            Vote.objects.create(user=request.user, time_option=time_option)

        return redirect('event_detail', event_id=event.id)
