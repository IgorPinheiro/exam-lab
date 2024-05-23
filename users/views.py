from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login
# Create your views here.

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha =  request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senha não está igual a confirmação, por favor tente novamente!' )
            return redirect('/users/cadastro')
        if len(senha) < 6:
            return redirect('/users/cadastro')
        
        if len(primeiro_nome) == 0 or len(email) == 0:
            messages.add_message(request, constants.ERROR, 'Nome ou email não podem ser vazios')
            return redirect('/users/cadastro')
        
        
        if User.objects.filter(username = username).exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe!' )
            return redirect('cadastro')
        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = username,
                email = email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, 'USUÁRIO CADASTRADO COM SUCESSO!')
        except:
            messages.add_message(request, constants.ERROR, 'Error no sistema, tente novamente')
            return redirect('/users/cadastro')
        
        return redirect('/users/cadastro')
    




def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
						# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/users/login')
