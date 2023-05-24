from django.urls import path
from . import views
from .models import Report
#from .views import get_unit_tree_data


urlpatterns = [
    path('', views.home),
    path('unit_tree_data/', views.get_unit_tree_data),
    path('unit/<int:node_id>/', views.unit, name='unit'),
    path('company/<int:node_id>/', views.company_view, name='company'),
    path('function/<int:node_id>/', views.function_view, name='function'),
    path('asset/<int:asset_id>/', views.asset_view, name='asset'),
    path('generate-pdf/<str:report_ids>/', views.generate_pdf, name='generate_pdf'),
    path('detailed-condition/<int:report_id>/', views.detailed_condition, name='detailed_condition'),
    path('about/', views.about),
    path('report/', views.report),
]