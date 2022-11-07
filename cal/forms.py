from csv import field_size_limit
from django.forms import ModelForm, DateInput
from django.contrib.auth.models import User
from cal.models import Event, Reason
from django.contrib.auth.forms import UserCreationForm, forms
# import forms

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      # 'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ['title', 'description', 'start_time', 'duration']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    # self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

      
class UserCreation(UserCreationForm):
    email = forms.EmailField(
    max_length=100,
    required = True,
    # help_text='Enter Email Address',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
  
    )

    '''first_name = forms.CharField(
    max_length=100,
    required = True,
    # help_text='Enter First Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )

    last_name = forms.CharField(
    max_length=100,
    required = True,
    # help_text='Enter Last Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )'''

    username = forms.CharField(
    max_length=200,
    required = True,
    # help_text='Enter Username',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )

    password1 = forms.CharField(
    # help_text='Enter Password',
    required = True,
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

    password2 = forms.CharField(
    required = True,
    # help_text='Enter Password Again',
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    labels = {
      'password1':'Password',
      'password2':'Confirm Password'
    }
    
class ReasonForm(ModelForm):
  class Meta:
    model = Reason
    fields = '__all__'