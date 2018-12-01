# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import json

import requests
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from requests_oauthlib import OAuth1
from . import forms
from .models import TwitterCredentails
from django.shortcuts import render


# Create your views here.

class CredentialsView(generic.FormView):
    template_name = "credentials.html"
    form_class = forms.CredentialsForm
    success_url = reverse_lazy("twitter:credentials")

    # model = TwitterCredentails


    def form_valid(self, form):
        print "credentail view get executed!!"
        access_token = self.request.POST['access_token']
        access_secret = self.request.POST['access_secret']
        consumer_key = self.request.POST['consumer_key']
        consumer_secret = self.request.POST['consumer_secret']
        try:
            tc = TwitterCredentails.objects.get(user=self.request.user)
            tc.access_token = access_token,
            tc.access_secret = access_secret,
            tc.consumer_key = consumer_key,
            tc.consumer_secret = consumer_secret
            tc.save()

        except TwitterCredentails.DoesNotExist:
            tc = TwitterCredentails(
                user=self.request.user,
                access_token=access_token,
                access_secret=access_secret,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret)

            tc.save()
        print "tc===", tc
        return super(CredentialsView, self).form_valid(form)


class HashTagSearchView(generic.TemplateView):
    template_name = "hashtag_serach.html"
    form_class = forms.HashTagSearchForm
    success_url = reverse_lazy("twitter:hashsearch")
    #context_object_name = 'context'

    # model = TwitterCredentails

    def form_valid(self, form, **kwargs):
        return super(HashTagSearchView, self).form_valid(form,)

    # def get(self, request, *args, **kwargs):
    #     form = self.form()
    #     return render(request,
    #                   self.get_template(),
    #                   {'form': form})

    def get(self, request, *args, **kwargs):
        #form = self.form()
        #context = super(HashTagSearchView, self).get_context_data(**kwargs)
        print "data===",request.GET
        if self.request.GET.get('hash_tag'):
            print "got hash tag======"
            hash_tag = self.request.POST['hash_tag']
            text_list = []
            url = "https://api.twitter.com/1.1/search/tweets.json?q=" + hash_tag + "&count=2"

            t = TwitterCredentails.objects.get(user=self.request.user)
            t1 = (t.consumer_key.encode("ascii"), t.consumer_secret.encode("ascii"),
                  t.access_token.encode("ascii"), t.access_secret.encode("ascii"))

            try:
                headeroauth = OAuth1(*t1)
                # signature_type='auth_header')
                print headeroauth.__dict__
                response = requests.get(url, auth=headeroauth)
                content = json.loads(response.content)
                for comment in content['statuses']:
                    text_list.append(comment.get('text'))
                #context['text_list']=text_list
                #print "text_list===",context
            except Exception as e:
                import traceback
                print traceback.format_exc()
            #print context
        return render(request,
                      self.template_name,
                      {'text_list':text_list})
