# -*- coding: utf-8 -*-

from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime

from cal.models import Event

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday, themonth, events):
        events_from_day = events.filter(day__day=day)
        events_html = '<ul>'
        for event in events_from_day:
            events_html += event.get_absolute_url() + '<br>'
        events_html += '</ul>'

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        elif day == date.today().day and themonth == date.today().month:
            return '<td class="today">%d%s</td>' % (day, events_html) # day outside month
        else:
            #return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
            return '<td class="day">%d%s</td>' % (day, events_html)


    def formatweek(self, themonth, theweek, events):
        s = ''.join(self.formatday(d, wd, themonth, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s # Number of day


    def formatmonth(self, request, theyear, themonth, withyear=True):
        events = Event.objects.filter(day__month=themonth, prop__user=request.user)

        v = []
        a = v.append
        a('<h3>' + self.formatmonthname(theyear, themonth, withyear=withyear) + '</h3>')
        a('\n')
        a('<table class="table-bordered">')
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(themonth, week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
