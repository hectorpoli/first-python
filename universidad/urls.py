from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'universidad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	
	url(r'^inicio/$', 'personas.views.index', name='inicio2' ),
	#url(r'^ingresoEstudiantes/$', 'personas.views.ingresoE',name='ingresoEstudiante' ), #name='ingresoE'
	url(r'^ingresoEstudiantes/(?P<id>\d+)?', 'personas.views.ingresoE', name='modificacionEstudiante' ),
	url(r'^ingresoProfesores/$', 'personas.views.ingresoP', name='ingresoP' ),
	url(r'^consultarEstudiantes/$', 'personas.views.consultar_estudiante', name='consultarEstudiante' ),
	url(r'^consultarProfesores/$', 'personas.views.consultar_profesor', name='consultarP' ),
	url(r'^generarpdf/(\d+)', 'personas.views.generar_pdf',name='pdf'),
    url(r'^admin/', include(admin.site.urls)),
)
