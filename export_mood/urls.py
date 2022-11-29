from django.urls import path
from . import views

urlpatterns = [
	path('', views.export_index, name='export_index'),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]