from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hola a todos. Esta es mi primera aplicación en Django")