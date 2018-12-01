# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

# Create your views here.


class SignUpView(generic.TemplateView):
    pass
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    """