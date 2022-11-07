from csv import field_size_limit
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from cal.models import Event, Reason
from django import forms

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

class CreateFormUser(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
  def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username)
        
        if user.exists():
            raise forms.ValidationError("Já existe um usuário com esse nome!")
        
        return self.cleaned_data.get('username')

  def clean_email(self):
      email = self.cleaned_data.get('email')
      model = self.Meta.model
      user = model.objects.filter(email__iexact=email)
      
      if user.exists():
          raise forms.ValidationError("Já existe um usuário com esse email!")
      
      return self.cleaned_data.get('email')


  def clean_password(self):
      password = self.cleaned_data.get('password1')
      password2 = self.data.get('password2')
      
      if password != password2:
          raise forms.ValidationError("Senhas diferentes!")

      return self.cleaned_data.get('password1')
  
class ReasonForm(ModelForm):
  class Meta:
    model = Reason
    fields = '__all__'
