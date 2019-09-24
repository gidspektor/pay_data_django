from django.urls import path
from . import views

urlpatterns = [
    path('', views.Payment_home.as_view(), name='payment-home'),
    path('api/', views.Api.as_view(), name='api'),
    path('search/', views.Payment_search.as_view(), name='payment-search'),
    path('detail-search/', views.Payment_detail_search.as_view(), name='payment-detail-search'),
    path('export-excel/', views.Export_to_excel.as_view(), name='export-excel')
]