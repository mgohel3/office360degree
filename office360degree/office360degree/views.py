from django.shortcuts import render

def index(request):
    return render(request, 'office360degree/index.html')