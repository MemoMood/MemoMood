from django.shortcuts import render, redirect
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from mood.models import UserDiary

# Create your views here.
content_type = 'application/pdf'

def get_data(request):
    user = request.user
    dict_return = {"username" : user}
    user_diary = UserDiary.objects.get(user=user)
    dict_diary = []
    for user in user_diary.diary.all():
        diary = {}
        diary['time'] = user.time
        # add mood string
        mood_str = ''
        mood_all = [str(m) for m in user.mood.all()]
        len_mood = len(mood_all)
        for m in range(len_mood):
            if m == len_mood-1:
                mood_str += str(mood_all[m])
            else:
                mood_str += str(mood_all[m]) + ','
        diary['mood'] = mood_str
        diary['place'] = user.place
        # add people string
        people_str = ''
        people_all = [str(m) for m in user.people.all()]
        len_people = len(people_all)
        for m in range(len_people):
            if m == len_mood-1:
                mood_str += str(people_all[m])
            else:
                mood_str += str(people_all[m]) + ','
        diary['people'] = people_str
        diary['weather'] = user.weather
        diary['text'] = user.text
        dict_diary.append(diary)
    dict_return['mood_data'] = dict_diary
    return dict_return


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
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
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


def export_index(request):
    context = {}
    return render(request, 'export_mood/index.html', context)
