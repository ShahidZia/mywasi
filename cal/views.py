# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import datetime
import calendar

from cal.forms import EventForm
from cal.models import Event
from cal.utils import EventCalendar

class EventView(View):
    template_name = 'calendar/calendar.html'

    def get(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}

        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()

        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month

        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month

        extra_context['previous_month'] = reverse('calendar') + '?day__gte=' + str(previous_month)
        extra_context['next_month'] = reverse('calendar') + '?day__gte=' + str(next_month)

        cal = EventCalendar()
        html_calendar = cal.formatmonth(self.request, d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="100"')
        extra_context['calendar'] = mark_safe(html_calendar)

        events = Event.objects.filter(day__gte = d)

        return render(self.request, self.template_name, {'extra_context': extra_context, 'events': events})


def event_view(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'calendar/event_view.html', {'event': event})


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm(instance=event)

    return render(request, 'calendar/event_edit.html', {'form': form})
