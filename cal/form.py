from django import forms
from .models import *
#crisssssssssss
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome", "email", "curso"]