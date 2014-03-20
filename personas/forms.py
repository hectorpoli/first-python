# -*- coding: utf-8 -*-
from personas.models import Profesor
from personas.models import Estudiante
from django.forms import ModelForm,forms
from django.forms import FileField,Select,TextInput
import re

class ProfesorForm(ModelForm):
	class Meta:
		model = Profesor
		
	def clean_cedula(self):
		data = self.cleaned_data['cedula']
		if not re.match("^(V|E)\d{7,8}",data):
			raise forms.ValidationError("El formato de la cédula no es válido!")
		return data

class EstudianteForm(ModelForm):
	class Meta:
		model = Estudiante
		
	def clean_cedula(self):
		data = self.cleaned_data['cedula']
		if not re.match("^(V|E)\d{7,8}",data):
			raise forms.ValidationError("El formato de la cédula no es válido!")
		return data
