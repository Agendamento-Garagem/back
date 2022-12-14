from datetime import datetime, timedelta, date
from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from .utils import Calendar


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

@login_required(login_url='cal:login')
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        obj = form.save(commit=False) # Return an object without saving to the DB
        obj.host = request.user # Add an author field which will contain current user's id
        obj.save() # Save the final "real form" to the DB
        return HttpResponseRedirect(reverse('cal:calendar'))

    return render(request, 'cal/event.html', {'form': form})

@login_required(login_url='cal:login')
def info_event(request, pk):
    evento = Event.objects.get(id=pk)
    
    if evento.pending == 0:
        evento.adm = str(request.user)
        evento.save()

    context = {'evento': evento}
    return render(request, 'cal/info.html', context)
    
@login_required(login_url='cal:login')
def delete_event(request, pk):
    evento = Event.objects.get(id=pk)
    context = {'evento': evento}

    if request.user != evento.host and not request.user.is_superuser:
        return('Voc?? n??o tem acesso a essa ??rea')
            
    if request.method == 'POST':
        evento.delete()
        return redirect('cal:calendar')
    
    return render(request, 'cal/delete.html', context)

def is_unique(email):
    objects = UserCreationForm.objects.all()
    print(objects)
    for user in objects:
        print(user)
        if user == email:
            print("falso")
            return False
    return True

# so falta checar o email repetido
def register(request):
    if request.user.is_authenticated:
        return redirect('cal:calendar')
    else:
        form = UserCreation()
        if request.method == 'POST':
            form = UserCreation(request.POST)
            if form.is_valid():
                form.save(commit=False)
                splitted = request.POST['email'].split('@')[1]
                if (splitted=='cesar.school' or splitted == 'cesar.org.br'):
                    form.save()

                    user = form.cleaned_data.get('username')
                    messages.success(request, 'A conta foi criada para ' + user)

                    return redirect('cal:login')
                else:
                    messages.error(request,"Email inv??lido")
                    return redirect('cal:register')

    context = {'form': form}
    return render(request, "cal/register.html", context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('cal:calendar')
    else:
        if(request.method == 'POST'):

            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                print('a')
                login(request, user)
                return redirect('cal:calendar')
            else:
                messages.info(request, "Usu??rio ou senha est?? incorreto.")

    context = {}       
    return render(request,'cal/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('cal:index')

def confirmation_event(request, pk):
    evento = Event.objects.get(id=pk)
    context = {'evento': evento}
    
    if request.method == 'POST':
        evento.pending = 1
        evento.save()
        return redirect('cal:calendar')

    return render(request, 'cal/confirm.html', context)

def deny_event(request, pk):
    evento = Event.objects.get(id=pk)
    form = ReasonForm()

    context = {'evento': evento, 'form':form}
    
    if request.method == 'POST':
        form = ReasonForm(request.POST)
        if(form.is_valid()):
            form.save()
        
        evento.reason = form.cleaned_data.get('reason')
        evento.pending = 2
        evento.save()
        return redirect('cal:calendar')

    return render(request, 'cal/deny.html', context)