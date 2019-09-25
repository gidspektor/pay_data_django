from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('user_home/', views.User_home.as_view(), name='user-home'),
    path('search/', views.Payment_search.as_view(), name='payment-search'),
    path('detail-search/', views.Payment_detail_search.as_view(), name='payment-detail-search'),
    path('export-excel/', views.Export_to_excel.as_view(), name='export-excel'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', views.Api.as_view(), name='api')
]