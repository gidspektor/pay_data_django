from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, TemplateView
from django.views import View
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
import requests, configparser, operator
from . import models, tools, forms
from functools import reduce
import pandas as pd

class Home(TemplateView):
  template_name = 'payment/home.html'

class User_home(LoginRequiredMixin, TemplateView):
  template_name = 'payment/user_home.html'

  def get_context_data(self, **kwargs):
    '''
    This takes in self and kwargs which is an object here.
    It sets context to have a an instance of the unregistered_user_form
    class and a comments_form class. It then returns the context.
    '''
    context = super(User_home, self).get_context_data(**kwargs)
    context['search_form'] = forms.Search_form()
    return context

class Payment_search(LoginRequiredMixin, ListView):
  context_object_name = 'people'
  template_name = 'payment/result.html'

  def get_queryset(self):
    form = forms.Search_form(self.request.GET)
    if form.is_valid():
      query = self.request.GET.get('query')
      people = models.Person_payment_information.objects.annotate(
        search = SearchVector(
          'person__first_name', 'person__last_name',
          'business_address_link__business__business',
          'business_address_link__address__city', 'business_address_link__address__country'
          )
      ).filter(search = SearchQuery(query))

      if len(people) == 0:
        messages.error(self.request, 'No results for your search')
      tools.write_to_excel_file(people)  
      return people

  def get_context_data(self, **kwargs):
    '''
    This takes in self and kwargs which is an object here.
    It sets context to have a an instance of the unregistered_user_form
    class and a comments_form class. It then returns the context.
    '''
    context = super(Payment_search, self).get_context_data(*kwargs)
    context['search_form'] = forms.Search_form()
    return context
    
class Payment_detail_search(LoginRequiredMixin, ListView):
  context_object_name = 'people'
  template_name = 'payment/result.html'

  def get_queryset(self):
    form = forms.Search_form(self.request.GET)
    if form.is_valid():
      query = self.request.GET.get('query')
      country = self.request.GET.get('country')
      business = self.request.GET.get('business')
      q_list = [Q(search = SearchQuery(query)), Q(search = SearchQuery(country)),
        Q(search = SearchQuery(business))]
      people = models.Person_payment_information.objects.annotate(
        search = SearchVector(
          'person__first_name', 'person__last_name',
          'business_address_link__business__business',
          'business_address_link__address__city', 'business_address_link__address__country'
          )
      ).filter(reduce(operator.and_, q_list))

      if len(people) == 0:
        messages.error(self.request, 'No results for your search')
      tools.write_to_excel_file(people)  
      return people

  def get_context_data(self, **kwargs):
    '''
    This takes in self and kwargs which is an object here.
    It sets context to have a an instance of the unregistered_user_form
    class and a comments_form class. It then returns the context.
    '''
    context = super(Payment_detail_search, self).get_context_data(*kwargs)
    context['search_form'] = forms.Search_form()
    return context

class Export_to_excel(LoginRequiredMixin, View):
  def get(self, request):
    with open('payment/excel/results.xls', 'rb') as file:
      data = file.read()
      response = HttpResponse(
        data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      )
      response['Content-Disposition'] = 'attachment; filename=results.xls'
    return response

class Api(LoginRequiredMixin, APIView):
  def get(self, request):
    config = configparser.ConfigParser()
    config.read('config.ini')
    r = requests.get(config['DEFAULT']['api'])
    self.post(r.json())

  def post(self, response):
    for item in response:
      if 'Covered Recipient Physician' in item.values():
        person, _ = models.Person.objects.get_or_create(
          profile_id = int(item['physician_profile_id']),
          first_name = item['physician_first_name'].lower(),
          last_name = item['physician_last_name'].lower()
        )
        address, _ = models.Address.objects.get_or_create(
          business_street = item['recipient_primary_business_street_address_line1'].lower(),
          city = item['recipient_city'].lower(),
          state = item['recipient_state'].lower(),
          country = item['recipient_country'].lower()
        )
        business, _ = models.Business.objects.get_or_create(
          business = item['submitting_applicable_manufacturer_or_applicable_gpo_name'].lower(),
        )
        business_address_link = models.Business_address_link.objects.create(
          business = business,
          address = address
        )
        business_address_link.save()
        payment = models.Payment.objects.create(
          record_id = int(item['record_id']),
          amount = float(item['total_amount_of_payment_usdollars']),
          date = item['date_of_payment'],
          number_of_payments = int(item['number_of_payments_included_in_total_amount']),
          payment_form = item['form_of_payment_or_transfer_of_value'],
          nature_of_payment = item['nature_of_payment_or_transfer_of_value']
        )
        payment.save()
        person_payment_information = models.Person_payment_information.objects.create(
          person = person,
          business_address_link = business_address_link,
          payment = payment
        )
        person_payment_information.save()
    return redirect('payment-home')