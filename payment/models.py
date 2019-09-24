from django.db import models
from datetime import datetime

class Custom_date_time_field(models.DateTimeField):
  def value_to_string(self, obj):
    value = self.value_from_object(obj)
    if value:
      datetime.strptime(value, '%Y%m%d %H:%M:%S')
      return value.isoformat()
    return ' '  

class Person(models.Model):
  profile_id = models.IntegerField(primary_key=True)
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)

  def __str__(self):
    return self.first_name

class Address(models.Model):
  id = models.AutoField(primary_key=True)
  business_street = models.CharField(max_length=100, unique=True)
  city = models.CharField(max_length=45)
  state = models.CharField(max_length=45)
  country = models.CharField(max_length=45)

  def __str__(self):
    return self.country

class Business(models.Model):
  id = models.AutoField(primary_key=True)
  business = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.business

class Business_address_link(models.Model):
  id = models.AutoField(primary_key=True)
  business = models.ForeignKey(Business, on_delete=models.CASCADE)
  address = models.ForeignKey(Address, on_delete=models.CASCADE) 

class Payment(models.Model):
  record_id = models.IntegerField(primary_key=True)
  amount = models.IntegerField()
  date = Custom_date_time_field()
  number_of_payments = models.IntegerField()
  payment_form = models.CharField(max_length=100)
  nature_of_payment = models.CharField(max_length=200)

class Person_payment_information(models.Model):
  id = models.AutoField(primary_key=True)
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  business_address_link = models.ForeignKey(Business_address_link, on_delete=models.CASCADE)
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE)