from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def action(request):
    data = {}
    data["id"] = 1
    data["username"] =  "Alpha"
    data["greet"] = "Hi, "+str(request.POST.get("command"))
    return JsonResponse(data)