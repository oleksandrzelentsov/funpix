from django.http import HttpResponse
from django.views import View
# from django.shortcuts import render


class MyView(View):
    def get(self, request):
        return HttpResponse('result')