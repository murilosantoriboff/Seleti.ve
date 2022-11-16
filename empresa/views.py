from django.shortcuts import render
from django.http import HttpResponse
from .models import Tecnologia, Empresa, Vagas
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404

def nova_empresa(request):

    if request.method == 'GET':
        techs = Tecnologia.objects.all()
        return render(request, 'nova_empresa.html', {'techs':techs})

    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        nicho = request.POST.get('nicho')
        caracteristicas = request.POST.get('caracteristicas')
        tecnologias = request.POST.getlist('tecnologias')
        logo = request.FILES.get('logo')

        if (len(nome.strip()) == 0 or len(email.strip()) == 0 or len(cidade.strip()) == 0 or len(endereco.strip()) == 0 or len(nicho.strip()) == 0 or len(caracteristicas.strip()) == 0 or (not logo)): 
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/home/nova_empresa')

        if logo.size > 100_000_000:
            messages.add_message(request, constants.ERROR, 'Sua logo ultrapassa o tamanho esperado')
            return redirect('/home/nova_empresa')

        if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
            messages.add_message(request, constants.ERROR, 'Nicho de mercado inválido')
            return redirect('/home/nova_empresa')

        empresa = Empresa(logo=logo,
                        nome=nome,
                        email=email,
                        cidade=cidade,
                        endereco=endereco,
                        nicho_mercado=nicho,
                        caracteristica_empresa=caracteristicas)

        empresa.save()
        empresa.tecnologias.add(*tecnologias)
        empresa.save()

        messages.add_message(request, constants.SUCCESS,'Nova Empresa Criada com Sucesso')
        return redirect('/home/nova_empresa')

def empresas(request):
    tecnologias = Tecnologia.objects.all()
    tecnologias_filtrar = request.GET.get('tecnologias')
    nome_filtrar = request.GET.get('nome')
    empresa = Empresa.objects.all()

    if tecnologias_filtrar:
        empresa = empresa.filter(tecnologias=tecnologias_filtrar)

    if nome_filtrar:
        empresa = empresa.filter(nome__icontains=nome_filtrar)

    return render(request, 'empresa.html', {'empresas': empresa, 'tecnologias':tecnologias})

def excluir_empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    empresa.delete()
    messages.add_message(request, constants.SUCCESS, 'Empresa Excluida com Sucesso')
    return redirect('/home/empresas')

def empresa(request, id):
    empresa_unica = get_object_or_404(Empresa, id=id)
    empresas = Empresa.objects.all
    tecnologias = Tecnologia.objects.all()
    vaga = Vagas.objects.filter(empresa_id=id)
    return render(request, 'empresa_unica.html', {'empresa_unica':empresa_unica, 'tecnologias':tecnologias, 'empresas':empresas, 'vagas':vaga})

