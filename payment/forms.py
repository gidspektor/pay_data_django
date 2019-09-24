from django import forms
import re

class Search_form(forms.Form):
  query = forms.CharField(label='search', required=True, max_length=100)