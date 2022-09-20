
from dataclasses import fields
from pyexpat import model
from tkinter import Label
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from administracion.models import Placa, Usuario


class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1','password2']


class PlacaForm(forms.ModelForm):
    class Meta:
        model = Placa
        fields = '__all__'
        
        