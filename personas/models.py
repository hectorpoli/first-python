# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import format_html

# Create your models here.


class Estado(models.Model):
	nombre = models.CharField(max_length=200,verbose_name="Estado")
	def __unicode__(self):
		return self.nombre
	
class Materia(models.Model):
	nombre = models.CharField(max_length=200,verbose_name="Materia")
	
	def __unicode__(self):
		return self.nombre
	
class Carrera(models.Model):
	nombre = models.CharField(max_length=200,verbose_name="Carrera")
	def __unicode__(self):
		return self.nombre
	
class Persona(models.Model):
	id_archivo = models.ForeignKey(Estado,verbose_name="Estado")
	nombre = models.CharField(max_length=200,verbose_name="Nombre")
	apellido = models.CharField(max_length=200,verbose_name="Apellido")
	cedula = models.CharField(max_length=9,verbose_name='Cédula',unique=True)
	direccion = models.TextField(verbose_name="Dirección")
	"""def __unicode__(self):
		return self.nombre"""
	
class Estudiante(Persona):
	carrera=models.ForeignKey(Carrera)
	descripcion = models.CharField(max_length=255,verbose_name="Descripción",blank=True)
	
class Profesor(Persona):
	materia=models.ForeignKey(Materia)
	descripcion = models.CharField(max_length=255,verbose_name="Descripción",blank=True)
	
	def materias(self):
		return format_html('<span style="color: red;">{0}</span>',self.materia)

	materias.allow_tags = True
	
