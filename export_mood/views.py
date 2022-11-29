from django.shortcuts import render, redirect
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from mood.models import UserDiary
from export_mood.function import *

# Create your views here.

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type=content_type)
    return None

# Opens up page as PDF


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        data = get_data(request)
        pdf = render_to_pdf('export_mood/pdf_form.html', data)
        return HttpResponse(pdf, content_type=content_type)


# Automatic downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        data = get_data(request)
        pdf = render_to_pdf('export_mood/pdf_form.html', data)

        response = HttpResponse(pdf, content_type=content_type)
        filename = "Diary_%s.pdf" % (request.user)
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response


def export_index(request):
    if not request.user.is_authenticated:
        return redirect('profile')
    context = {}
    return render(request, 'export_mood/index.html', context)
