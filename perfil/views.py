from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

@login_required
def perfil(request):
    form = FuncionarioForm(request.POST)
    
    return render(request, 'perfil/perfil.html', {})
