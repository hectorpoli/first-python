from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from forms import ProfesorForm,EstudianteForm
from personas.models import Estudiante,Profesor
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A3, A4, landscape, portrait
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO



# Create your views here.

def index(request):
	html = '<br>Hola mundo</br>'
	return HttpResponse(html)
"""	
def ingresoE(request):
	if request.method == "POST":
		form = EstudianteForm(request.POST)
		if form.is_valid():
			form.save()
			form = EstudianteForm()
			
	else:
		form = EstudianteForm()
	return render_to_response('ingresoE.html',{'form':form},context_instance=RequestContext(request))
"""

def ingresoE(request,id='',template_name='ingresoE.html'):
	if id:
		est = get_object_or_404(Estudiante,pk=id) # Estudiante.objects.get(pk=id)
	else:
		est= None
		
	if request.method == "POST":
		form = EstudianteForm(request.POST,instance=est)
		if form.is_valid():
			form.save()
			#form = EstudianteForm()
			messages.add_message(request, messages.SUCCESS, 'Estudiante modificado correctamente.')
			redirect_url = reverse('consultarEstudiante')
			return HttpResponseRedirect(redirect_url)
			
	else:
		form = EstudianteForm(instance=est)
	
	return render_to_response(template_name,{'form':form,'id':id},context_instance=RequestContext(request))

"""
def ingresoP(request):
	if request.method == "POST":
		form = ProfesorForm(request.POST)
		if form.is_valid():
			form.save()
			form = ProfesorForm()
	else:
		form = ProfesorForm()
	return render_to_response('ingresoP.html',{'form':form},context_instance=RequestContext(request))
"""

def ingresoP(request,id='',template_name='ingresoP.html'):
	if id:
		est = get_object_or_404(Profesor,pk=id) # Profesor.objects.get(pk=id)
	else:
		est= None
		
	if request.method == "POST":
		form = ProfesorForm(request.POST,instance=est)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Profesor modificado correctamente.')
			redirect_url = reverse('consultarProfesor')
			return HttpResponseRedirect(redirect_url)
			
	else:
		form = ProfesorForm(instance=est)
	
	return render_to_response(template_name,{'form':form,'id':id},context_instance=RequestContext(request))
	

def consultar_estudiante(request,pagina=''):
	estudiante_list = Estudiante.objects.all()
	paginator = Paginator(estudiante_list, 2)
	#page = request.GET.get('page')
	
	if pagina:
		page=pagina
	else:
		page = request.GET.get('page')
	
	try:
		estudiantes = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		estudiantes = paginator.page(1)
	except EmptyPage:
		# SI LA PAGINA SOBRE PASA EL ULTIMO ELEMENTO LO COLOCAMOS
		estudiantes = paginator.page(paginator.num_pages)
	context = RequestContext(request)
	
	if not pagina:
		return render_to_response('consultarE.html',{'estudiantes':estudiantes},context_instance=context)
	else:
		return estudiantes
	

def consultar_profesor(request,pagina=''):
	profesor_list = Profesor.objects.all()
	paginator = Paginator(profesor_list, 2)
	#page = request.GET.get('page')
	
	if pagina:
		page=pagina
	else:
		page = request.GET.get('page')
	
	try:
		profesores = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		profesores = paginator.page(1)
	except EmptyPage:
		# SI LA PAGINA SOBRE PASA EL ULTIMO ELEMENTO LO COLOCAMOS
		profesores = paginator.page(paginator.num_pages)
	context = RequestContext(request)
	
	if not pagina:
		return render_to_response('consultarP.html',{'profesores':profesores},context_instance=context)
	else:
		return profesores
	
def generar_pdf_estudiante(request,page):
	elements = []
	styles=getSampleStyleSheet()
	styleN = styles["Normal"]
	styleN.alignment = TA_RIGHT
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	# Creamos el HttpResponse con las cabeceras del proyecto.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="estudiante.pdf"'
	
	buffer = BytesIO()
	
	# Create the PDF object, using the response object as its "file."
	doc = SimpleDocTemplate(response, pagesize=A4)
	data = []
	# Cabeceras
	data.append([Paragraph('''<b>Nombre</b>''', styleBH),
	Paragraph('''<b>Apellido</b>''', styleBH),
	Paragraph('''<b>C&eacute;dula</b>''', styleBH),
	Paragraph('''<b>Direcci&oacute;n</b>''', styleBH),
	Paragraph('''<b>Carrera</b>''', styleBH),
	Paragraph('''<b>Descripci&oacute;n</b>''', styleBH)])
	
	 # Reporte
	estudiantes = consultar_estudiante(request,page)
	for e in estudiantes:
		data.append([Paragraph(e.nombre, styleN),
		Paragraph(e.apellido, styleN),
		Paragraph(e.cedula, styleN),
		Paragraph(e.direccion, styleN),
		Paragraph(e.carrera.nombre, styleN),
		Paragraph(e.descripcion, styleN)])
	table = Table(data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,3* cm, 3 * cm,3 * cm],repeatRows=1)
	table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	('BOX', (0,0), (-1,-1), 0.25, colors.black),
	('BACKGROUND',(0,0),(-1,0),colors.springgreen)]))
	
	elements = [table]
	doc.build(elements)
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response	
	
	
def generar_pdf_profesor(request,page):
	elements = []
	styles=getSampleStyleSheet()
	styleN = styles["Normal"]
	styleN.alignment = TA_RIGHT
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	# Creamos el HttpResponse con las cabeceras del proyecto.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="profesor.pdf"'
	
	buffer = BytesIO()
	
	# Create the PDF object, using the response object as its "file."
	doc = SimpleDocTemplate(response, pagesize=A4)
	data = []
	# Cabeceras
	data.append([Paragraph('''<b>Nombre</b>''', styleBH),
	Paragraph('''<b>Apellido</b>''', styleBH),
	Paragraph('''<b>C&eacute;dula</b>''', styleBH),
	Paragraph('''<b>Direcci&oacute;n</b>''', styleBH),
	Paragraph('''<b>Materia</b>''', styleBH),
	Paragraph('''<b>Descripci&oacute;n</b>''', styleBH)])
	
	 # Reporte
	profesor = consultar_profesor(request,page)
	for e in profesor:
		data.append([Paragraph(e.nombre, styleN),
		Paragraph(e.apellido, styleN),
		Paragraph(e.cedula, styleN),
		Paragraph(e.direccion, styleN),
		Paragraph(e.materia.nombre, styleN),
		Paragraph(e.descripcion, styleN)])
	table = Table(data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,3* cm, 3 * cm,3 * cm],repeatRows=1)
	table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	('BOX', (0,0), (-1,-1), 0.25, colors.black),
	('BACKGROUND',(0,0),(-1,0),colors.springgreen)]))
	
	elements = [table]
	doc.build(elements)
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response	
