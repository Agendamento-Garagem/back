from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from . models import Event, Usuario
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import *
from .utils import Calendar
from .forms import EventForm

def index(request):
    return render(request, 'cal/index.html')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})

def info_event(request, pk):
    evento = Event.objects.get(id=pk)
    context = {'evento': evento}
    return render(request, 'cal/info.html', context)
    

def delete_event(request, pk):
    evento = Event.objects.get(id=pk)
    context = {'evento': evento}

    if request.method == 'POST':
        evento.delete()
        return redirect('cal:calendar')
    
    return render(request, 'cal/delete.html', context)
    return HttpResponse('deus me ajuda') 

#crisssssssssssssssss
def create(request):
    return render(request, "cal/create.html")

def painel(request):
    return render(request,'cal/painel.html')


def store(request):
    data = {}
    if(request.POST['password'] != request.POST['password-conf']):
        data['msg'] = 'Senha e confirmação de senha diferentes!'
        data['class'] = 'alert-danger'
    else:
        user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
        data['msg'] = 'Usuário cadastrado com sucesso!'
        data['class'] = 'alert-danger'
    return render(request, "cal/create.html",data)

def dologin(request):
    data = {}
    user = authenticate(username=request.POST['user'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect('/calendar/')
    else:
        data['msg'] = 'Usuário ou Senha inválidos!'
        data['class'] = 'alert-danger'
        return render(request,'cal/painel.html', data)
    
def dashboard(request):
    return HttpResponse('jason deruloooo')