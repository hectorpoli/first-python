from django.contrib import admin

# Register your models here.

from models import Estado,Materia,Carrera,Estudiante,Profesor


class EstadoAdmin(admin.ModelAdmin):
	pass

class MateriaAdmin(admin.ModelAdmin):
	pass

class CarreraAdmin(admin.ModelAdmin):
	pass

class EstudianteAdmin(admin.ModelAdmin):
	list_display = ('nombre','apellido')

class ProfesorAdmin(admin.ModelAdmin):
	list_display = ('nombre','apellido','descripcion','materias')
	
admin.site.register(Estado,EstadoAdmin)
admin.site.register(Materia,MateriaAdmin)
admin.site.register(Carrera,CarreraAdmin)
admin.site.register(Estudiante,EstudianteAdmin)
admin.site.register(Profesor,ProfesorAdmin)
