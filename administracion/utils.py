from io import BytesIO
import io
from django.http import HttpResponse
from django.template.loader import get_template

import uuid

from datetime import datetime

from xhtml2pdf import pisa

def render_to_pdf(template_src,context_dict={}): 
    template= get_template(template_src)
    html=template.render(context_dict)
    result=io.BytesIO()
    pdf=pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None
 
 
 


def obtener_uuid():
    return str(uuid.uuid4())


def fecha_y_hora():
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S | https://parzibyte.me/blog")
    return fecha


def fecha_y_hora_para_nombre_archivo():
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d_%H-%M-%S")
    return fecha