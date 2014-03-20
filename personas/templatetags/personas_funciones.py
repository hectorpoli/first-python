from django import template

register = template.Library()

def generar_paginacion(registros):
	paginacion = ""
	
	if registros.has_previous():
		paginacion+='<a href="?page=%s">Anterior</a>' %registros.previous_page_number()
	
	paginacion+= '<span class="current">'
	
	for p in registros.paginator.page_range:
		if p == registros.number:
			paginacion+= '<a>%s</a>' % p
		else:
			paginacion+= '<a href="?page=%s">%s</a>' % (p,p)
	paginacion+= '</span>'
		
	if registros.has_next():
		paginacion+= '<a href="?page=%s">Siguiente</a>' % registros.next_page_number()
		
	return paginacion
		
register.simple_tag(generar_paginacion)
