from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.

def test_view(request):
    return render(request, 'wrkout/base.html')
