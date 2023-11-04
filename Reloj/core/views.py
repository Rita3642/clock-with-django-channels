from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.

def reloj(request):

    with open('/home/rita/Escritorio/RelojMundial/Reloj/Reloj/timezone.json', 'r') as json_file:
        timezone = json.load(json_file)

    countries =  timezone['zonas_horarias']

    context = {
        'countries': countries,
    }

    return render(request, 'reloj.html', context)




