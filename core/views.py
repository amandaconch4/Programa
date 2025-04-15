from django.shortcuts import render

# Create your views here.

def sevengamer(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def terror(request):
    return render(request, 'terror.html')

def mundoabierto(request):
    return render(request, 'mundo-abierto.html')

def accion(request):
    return render(request, 'accion.html')

def carreras(request):
    return render(request, 'carreras.html')

def deportes(request):
    return render(request, 'deportes.html')

def rol(request):
    return render(request, 'rol.html')

def registro(request):
    return render(request, 'registro.html')

def admin(request):
    return render(request, 'admin.html')