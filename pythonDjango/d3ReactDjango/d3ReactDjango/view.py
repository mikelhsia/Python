from django.shortcuts import render

def goToHomeIndex(request):
    return render(request, 'home.html')