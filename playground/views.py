from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    x = 1
    y = 2
    z = calculate()
    return render(request, 'hello.html', {'name': 'Emily'})
    # return HttpResponse('Hello World!')

def calculate(): 
    x = 1
    x = 2
    return x