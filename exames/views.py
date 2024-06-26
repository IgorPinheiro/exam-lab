from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExame
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants

@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET":
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    elif request.method == 'POST':
        exames_id = request.POST.getlist('exames')

        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        #preco_total = solicitacao_exames.aggregate(total=Sum('preco'))['total']

        # Calcular preço dos examens disponíveis

        preco_total = 0
        for solicitacao_exame in solicitacao_exames:
            if solicitacao_exame.disponivel:
                preco_total += solicitacao_exame.preco
        
        
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames, 
                                                         'solicitacao_exames': solicitacao_exames, 
                                                         'preco_total': preco_total,
                                                         'data_agora': datetime.now() })
@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exame')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
    
    pedido_exame = PedidosExames(
        usuario=request.user,
        data=datetime.now()
    )
    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario = request.user,
            exame = exame,
            status = 'E',
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)
    pedido_exame.save()
    messages.add_message(request, constants.SUCCESS, f'Pedido realizado com sucesso')

    return redirect('/exames/gerenciar_pedidos')

@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect('/exames/gerenciar_pedidos/')

    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido excluido com sucesso')
    return redirect('/exames/gerenciar_pedidos/')