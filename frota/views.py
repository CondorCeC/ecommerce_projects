from django.shortcuts import render, reverse, redirect, get_object_or_404
from frota.models import Entrega, EntregaLog, Insucesso
from django.core.paginator import Paginator
from frota.forms import EntregaForm, PictureForm, InsucessoForm
from django.utils import timezone
from django.contrib import messages
import requests
from django.contrib.auth.models import Group
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.db.models import Q
from django.http import HttpResponse
import openpyxl
import pytz
from datetime import datetime
from email.mime.base import MIMEBase
from email import encoders
import os
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, IntegerField
from datetime import datetime, timedelta

def construct_google_maps_url_with_addresses(addresses):
    base_url = "https://www.google.com/maps/dir/"
    formatted_addresses = '/'.join(addresses)
    return f"{base_url}{formatted_addresses}"

def get_address_from_coordinates(lat, lng):
    API_KEY = 'AIzaSyDt1VI64EJPMb_nfNIom_tL92VqconyOPU'
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(base_url, params={
        "latlng": f"{lat},{lng}",
        "key": API_KEY
    })
    
    data = response.json()
    if data['results']:
        return data['results'][0]['formatted_address']
    return None

def remove_ent(request, entrega_id):
    if request.method == 'GET':
        entrega = get_object_or_404(Entrega, pk=entrega_id)
        entrega.status = "Exportado"
        entrega.save()
    return redirect('entrega:selected_entregas')

def update_entrega_status(request):
    if request.method == 'GET':
        selected_entregas_ids = request.GET.getlist('selected_contacts')
        if selected_entregas_ids:
            selected_entregas = Entrega.objects.filter(id__in=selected_entregas_ids)
            for entrega in selected_entregas:
                entrega.status = "Em Rota"
                entrega.save()
    return redirect('entrega:selected_entregas')


def create_entrega(request):
    owner = request.user
    form_action = reverse('entrega:create_entrega')
    if request.method == 'POST':
        form = EntregaForm(request.POST, request.FILES, initial={'user': owner}) #
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.data_ent = timezone.now()
            
            if not entrega.owner: 
                group = entrega.group 
                users = group.user_set.all() 
                entrega.owner = users.first() 

            entrega.save()
            return redirect('entrega:index_entrega')
    else:
        if owner.is_superuser:
            form = EntregaForm(initial={'user': owner})
        else:
            form = EntregaForm(initial={'user': owner})
            form.fields['group'].queryset = request.user.groups.all()

    context = {
        'form': form,
        'form_action': form_action,
    }
    return render(request, 'frota/create_entrega.html', context)


def email_track(email_destinatario, nome, numero_pedido):
    smtp_server = 'smtp.condor.com.br'
    smtp_port = 587
    smtp_username = 'sac.cec'
    smtp_password = 'PXGf@3PU'
    template = """
        Olá {nome},

        Motorista coletou o seu pedido 
        {pedido} na loja para entrega!
        Atenciosamente,
        Equipe do Condor em Casa
        """
    remetente = 'sac.cec@condor.com.br'
    destinatario = email_destinatario
    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = remetente
    mime_multipart['to'] = destinatario
    mime_multipart['subject'] = 'Entregas - Condor em Casa'

    corpo_email = MIMEText(template.format(nome=nome, pedido=numero_pedido), 'plain')
    mime_multipart.attach(corpo_email)


    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.send_message(mime_multipart)

def rota(request):
    if request.method == 'POST':
        
        selected_ent_ids = request.POST.getlist('selected_ent')
        
        for ent_id in selected_ent_ids:
            email = request.POST.get(f'email_{ent_id}')
            pedido = request.POST.get(f'pedido_{ent_id}')
            nome = request.POST.get(f'nome_{ent_id}')
          
            email_track(email, nome, pedido)
            
        lat = request.POST.get('starting_point_lat')
        lng = request.POST.get('starting_point_lng')
        selected_contacts_ids = request.POST.getlist('selected_ent')
        selected_contacts = Entrega.objects.filter(id__in=selected_contacts_ids)
        base_url = "https://www.google.com/maps/dir/"
        locations = [f'{lat},{lng}']
        
        for contact in selected_contacts:
            locations.append(contact.endereco.replace(" ", "+"))

        url = base_url + "/".join(locations)
        
        return redirect(url)



def entrega(request, entrega_id):
    user_name = request.user.get_username()
    stamp = timezone.now()
    single_entrega = get_object_or_404(Entrega, pk=entrega_id, show=True)
    owner = request.user
    if owner.is_superuser:
        single_entrega = get_object_or_404(Entrega, pk=entrega_id, show=True) 
    else:
        single_entrega = get_object_or_404(Entrega, pk=entrega_id, show=True, group__in=request.user.groups.all())
    if request.method == 'POST':
        if 'obs' in request.POST:
            observacao = request.POST.get('obs')
            single_entrega.description_store = observacao
            single_entrega.save()
            EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Adicionou: {observacao}")
            messages.success(request, 'Obrigado pelo retorno!')
        elif 'picture' in request.FILES:
            form = PictureForm(request.POST, request.FILES, instance=single_entrega)
            if form.is_valid():
                form.save()
                messages.success(request, 'Imagem salva com sucesso!')
                
    site_title = f'{single_entrega.first_name} {single_entrega.numero_pedido} - '
    context = {
        'entrega': single_entrega,
        'site_title': site_title,
        'observacao': single_entrega.description_store,
    }

    return render(request, 'frota/detalhe_entrega.html', context)


def detalhamento(request):
    owner = request.user
    user_profile = request.user.userprofile
    user_groups = request.user.groups.all()
    all_stores = user_groups
    q_objects = Q(entrega__group__in=user_groups)
    
    if user_profile.role == 'S':
        q_objects &= Q(user=owner) & (Q(action__icontains="Finalizou a entrega em") | 
                                    Q(action__icontains="Nova tentativa de entrega em") | 
                                    Q(action__icontains="Fez uma tentativa de entrega em"))
        all_drivers = User.objects.filter(userprofile__role='M')

    else:
        q_objects &= Q(user=owner) & Q(action__icontains="Finalizou a entrega em")
        all_drivers = User.objects.filter(id=owner.id)

    filter_driver_id = request.GET.get('filter_driver')
    filter_store_id = request.GET.get('filter_store')

    if filter_driver_id:
        q_objects &= Q(entrega__owner_id=filter_driver_id)
    if filter_store_id:
        q_objects &= Q(entrega__group_id=filter_store_id)

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        q_objects &= Q(timestamp__gte=start_date)
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() + timedelta(days=1)
        q_objects &= Q(timestamp__lt=end_date)
    logs_entrega = EntregaLog.objects.filter(q_objects).order_by('-timestamp')

    context = {
        'logs_entrega': logs_entrega,
        'all_drivers': all_drivers,
        'all_stores': all_stores,
        'filter_driver_id': filter_driver_id,  
        'filter_store_id': filter_store_id, 
    }
    
    return render(request, 'frota/detalhamento.html', context)



def selected_entregas(request):
    
    owner = request.user
    desired_statuses = ['Em Rota', 'Tentativa']
    selected_loja = request.GET.get("loja")
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not start_date_str:
        start_date = datetime.now().date() - timedelta(days=3)
    else:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

    if not end_date_str:
        end_date = datetime.now().date() + timedelta(days=2)
    else:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    base_query = Q(show=True, status__in=desired_statuses, data_ent__date__range=(start_date, end_date))

    janela_ordering = Case(
        When(janela='09:00 às 13:00', then=Value(1)),
        When(janela='09:00 às 14:00', then=Value(2)),
        When(janela='12:00 às 17:00', then=Value(3)),
        When(janela='13:00 às 17:00', then=Value(4)),
        When(janela='14:00 às 20:00', then=Value(5)),
        When(janela='17:00 às 20:00', then=Value(6)),
        default=Value(0),
        output_field=IntegerField()
    )

    if owner.is_superuser:
        if selected_loja and selected_loja != "Todas":
            loja_group = Group.objects.get(name=selected_loja)
            entregas = Entrega.objects.filter(base_query & Q(group=loja_group)).annotate(
                janela_order=janela_ordering
            ).order_by('-status', 'data_ent')
        else:
            entregas = Entrega.objects.filter(base_query).annotate(
                janela_order=janela_ordering
            ).order_by('-status', 'data_ent')
    else:
        if selected_loja and selected_loja != "Todas":
            loja_group = Group.objects.get(name=selected_loja)
            entregas = Entrega.objects.filter(base_query & Q(group=loja_group)).annotate(
                janela_order=janela_ordering
            ).order_by('-status', 'data_ent')
        else:
            entregas = Entrega.objects.filter(base_query & Q(group__in=request.user.groups.all())).annotate(
                janela_order=janela_ordering
            ).order_by('-status', 'data_ent')

    user_groups = request.user.groups.all()
    paginator = Paginator(entregas, 40)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    insucessos = {entrega.id: entrega.insucessos.all() for entrega in entregas}
    
    context = {
        'page_obj': page_obj,
        'site_title': 'Minhas Entregas - ',
        'user_groups': user_groups,
        'selected_loja': selected_loja,
        'insucessos': insucessos,
        #'selected_date': selected_date  
    }
    
    return render(request, 'frota/ent_select.html', context)

def index_entrega(request):
   
    owner = request.user
    desired_statuses = ['Exportado', 'Emitido']
    selected_loja = request.GET.get("loja")
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not start_date_str:
        start_date = datetime.now().date() - timedelta(days=3)
    else:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

    if not end_date_str:
        end_date = datetime.now().date() + timedelta(days=2)
    else:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    janela_ordering = Case(
        When(janela='09:00 às 13:00', then=Value(1)),
        When(janela='09:00 às 14:00', then=Value(2)),
        When(janela='12:00 às 17:00', then=Value(3)),
        When(janela='13:00 às 17:00', then=Value(4)),
        When(janela='14:00 às 20:00', then=Value(5)),
        When(janela='17:00 às 20:00', then=Value(6)),
        default=Value(0),
        output_field=IntegerField()
    )
    base_query = Q(show=True, status__in=desired_statuses, data_ent__date__range=(start_date, end_date))
    if owner.is_superuser:
        if selected_loja and selected_loja != "Todas":
            loja_group = Group.objects.get(name=selected_loja)
            entregas = Entrega.objects.filter(base_query & Q(group=loja_group)).annotate(
                janela_order=janela_ordering,
            ).order_by('-status', 'data_ent')
        else:
            entregas = Entrega.objects.filter(base_query).annotate(
                janela_order=janela_ordering,
            ).order_by('-status', 'data_ent')
    else:   
        if selected_loja and selected_loja != "Todas":
            loja_group = Group.objects.get(name=selected_loja)
            entregas = Entrega.objects.filter(base_query & Q(group=loja_group)).annotate(
                janela_order=janela_ordering,
            ).order_by('-status', 'data_ent')
        else:
            entregas = Entrega.objects.filter(base_query & Q(group__in=request.user.groups.all())).annotate(
                janela_order=janela_ordering,
            ).order_by('-status', 'data_ent')

    user_groups = request.user.groups.all()
    paginator = Paginator(entregas, 40)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'site_title': 'Entregas - ',
        'user_groups': user_groups,
        'selected_loja': selected_loja,
    }
    return render(request, 'frota/index_frota.html', context)


def insucesso(request, entrega_id):
    single_entrega = get_object_or_404(Entrega, pk=entrega_id)
    owner = request.user

    if request.method == 'POST':
        action_type = request.POST.get('action_type')
      
        if action_type == 'devolver':
            form = InsucessoForm(request.POST, request.FILES)
            if form.is_valid():
                insucesso = form.save(commit=False)
                insucesso.entrega = single_entrega
                single_entrega.status = 'Exportado'
                insucesso.hora_ins = timezone.now()

                final_lat2 = request.POST.get('final_lat2')
                final_lng2 = request.POST.get('final_lng2')
                
                if 'obs_insucesso' in request.POST:
                    observacao_insucesso = request.POST.get('obs_insucesso')
                    insucesso.description_ins = observacao_insucesso
                
                if final_lat2 and final_lng2:
                    insucesso.final_lat2 = final_lat2
                    insucesso.final_lng2 = final_lng2
                    address = get_address_from_coordinates(final_lat2, final_lng2) 
                    insucesso.end_ins = address

                insucesso.save()
                single_entrega.save()
                email_insucesso(single_entrega)
                EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Adicionou : {observacao_insucesso}")
                EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Nova tentativa de entrega em : {address}")
                return redirect('entrega:selected_entregas')
            else:
                messages.error(request, 'Erro ao salvar a imagem.')
                return redirect('entrega:selected_entregas') 

        elif action_type == 'insucesso':
            form = InsucessoForm(request.POST, request.FILES)
            if form.is_valid():
                insucesso = form.save(commit=False)
                insucesso.entrega = single_entrega
                single_entrega.status = 'Tentativa'
                insucesso.hora_ins = timezone.now()

                final_lat2 = request.POST.get('final_lat2')
                final_lng2 = request.POST.get('final_lng2')
                
                if 'obs_insucesso' in request.POST:
                    observacao_insucesso = request.POST.get('obs_insucesso')
                    insucesso.description_ins = observacao_insucesso
                    

                if final_lat2 and final_lng2:
                    insucesso.final_lat2 = final_lat2
                    insucesso.final_lng2 = final_lng2
                    address = get_address_from_coordinates(final_lat2, final_lng2) 
                    insucesso.end_ins = address

                insucesso.save()
                single_entrega.save() 
                email_insucesso(single_entrega)
                EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Adicionou : {observacao_insucesso}")
                EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Fez uma tentativa de entrega em : {address}")
                return redirect('entrega:selected_entregas')
            else:
                messages.error(request, 'Erro ao salvar a imagem.')
                return redirect('entrega:selected_entregas') 

        else:
            messages.error(request, 'Método não suportado!')
            return redirect('entrega:selected_entregas')

def finalizar_entrega(request, entrega_id):
    owner = request.user
    user_name = request.user.get_username()
    stamp = timezone.now()
    single_entrega = get_object_or_404(Entrega, pk=entrega_id)
    if request.method == 'POST':
        if owner.is_superuser:
            if 'picture' in request.FILES:
                form = PictureForm(request.POST, request.FILES, instance=single_entrega)
                if form.is_valid():
                    form.save()
                else:
                    messages.error(request, 'Erro ao salvar a imagem.')
                    return redirect('entrega:selected_entregas') 
            else:
       
                messages.error(request, 'Uma imagem é obrigatória para finalizar a entrega.')
                return redirect('entrega:selected_entregas') 
        
            if 'obs' in request.POST:
                observacao = request.POST.get('obs')
                single_entrega.description_store = observacao
                single_entrega.save()
                EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Adicionou: {observacao}")
            else:
                messages.error(request, 'Observação Obrigatória!')
                return redirect('entrega:selected_entregas')     
            
            single_entrega.status = 'Concluído'
            single_entrega.timestamp = timezone.now()
            final_lat = request.POST.get('final_lat')
            final_lng = request.POST.get('final_lng')
           
            if final_lat and final_lng:
                single_entrega.final_lat = final_lat
                single_entrega.final_lng = final_lng
                address = get_address_from_coordinates(final_lat, final_lng)
                single_entrega.end_final = address
            single_entrega.save()
            EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Finalizou a entrega em : {address}")
            messages.success(request, 'Entrega Concluída!')
            return redirect('entrega:selected_entregas')
        
        else:
            if 'picture' in request.FILES:
                form = PictureForm(request.POST, request.FILES, instance=single_entrega)
                if form.is_valid():
                    form.save()
            if 'obs' in request.POST:
                observacao = request.POST.get('obs')
                single_entrega.description_store = observacao
                single_entrega.save()
                EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Adicionou: {observacao}")

            else:
                messages.error(request, 'Observação Obrigatória!')
                return redirect('entrega:selected_entregas')  
            single_entrega.status = 'Concluído'
            single_entrega.timestamp = timezone.now()
            final_lat = request.POST.get('final_lat')
            final_lng = request.POST.get('final_lng')
         
            if final_lat and final_lng:
                single_entrega.final_lat = final_lat
                single_entrega.final_lng = final_lng
                address = get_address_from_coordinates(final_lat, final_lng)
                single_entrega.end_final = address
            single_entrega.save()
            EntregaLog.objects.create(entrega=single_entrega, user=owner, action=f"Finalizou a entrega em : {address}")
            messages.success(request, 'Entrega Concluída!')
            return redirect('entrega:selected_entregas')

def email_insucesso(single_entrega):
    insucesso = single_entrega.insucessos.last()

    smtp_server = 'smtp.condor.com.br'
    smtp_port = 587
    smtp_username = 'sac.cec'
    smtp_password = 'PXGf@3PU'
    pedido = single_entrega.numero_pedido
    loja = single_entrega.group
    owner = single_entrega.owner
    obs_ent = insucesso.description_ins
    cliente_nome = single_entrega.first_name
    cliente_tel = single_entrega.phone
    img_ins = insucesso.img_insucesso
    hr_ins = datetime.now()
    end_ins = insucesso.end_ins
    formatted_hr_ins = hr_ins.strftime('%Y-%m-%d %H:%M:%S')
    with open('base_templates/global/email3.html', 'r', encoding='utf-8') as file:
        template = file.read()
    template = template.replace('{{loja}}', str(loja))
    template = template.replace('{{owner}}', str(owner))
    template = template.replace('{{obs_ent}}', obs_ent)
    template = template.replace('{{pedido}}', pedido)
    template = template.replace('{{formatted_hr_ins}}', str(formatted_hr_ins))
    template = template.replace('{{end_ins}}', end_ins)
    template = template.replace('{{cliente_nome}}', cliente_nome)
    template = template.replace('{{cliente_tel}}', cliente_tel)
    remetente = 'sac.cec@condor.com.br'
    destinatario = 'at2.cec@condor.com.br'
    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = remetente
    mime_multipart['to'] = destinatario
    mime_multipart['subject'] = 'Entregas - Condor em Casa'
    corpo_email = MIMEText(template, 'html', 'utf-8')
    mime_multipart.attach(corpo_email)
    attachment = MIMEBase('application', 'octet-stream')
    with open(img_ins.path, 'rb') as file:

        attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(img_ins.path)}')

    mime_multipart.attach(attachment)
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.send_message(mime_multipart)

def export_to_excel(request):
    if request.method == "POST":
        selected_logs_ids = request.POST.getlist('selected_logs')
        entrega_logs = EntregaLog.objects.filter(id__in=selected_logs_ids).order_by('entrega_id', 'timestamp')
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="entregas_selecionadas.xlsx"'
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        headers = ["Contagem", "ID Entrega", "Pedido", "Tipo de Entrega", "Data", "Grupo"]
        for col_num, header_title in enumerate(headers, 1):
            column_letter = openpyxl.utils.get_column_letter(col_num)
            worksheet[f'{column_letter}1'] = header_title
        for row_num, log in enumerate(entrega_logs, 2):
            entrega = log.entrega
            worksheet[f'A{row_num}'] = row_num - 1 
            worksheet[f'B{row_num}'] = entrega.id
            worksheet[f'C{row_num}'] = entrega.numero_pedido
            if "Finalizou a entrega em" in log.action:
                worksheet[f'D{row_num}'] = "Entrega"
            else:
                worksheet[f'D{row_num}'] = "Reentrega"
            worksheet[f'E{row_num}'] = log.timestamp.astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
            worksheet[f'F{row_num}'] = entrega.group.name if entrega.group else ''
        workbook.save(response)
        return response
    return HttpResponse("Método não permitido", status=405)

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
def login_entrega(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('entrega:index_entrega')
        messages.error(request, 'Login inválido')
    return render(
        request,
        'frota/login_entrega.html',
        {
            'form': form
        }
    )
@login_required(login_url='entrega:login_entrega')
def logout_entrega(request):
    auth.logout(request)
    return redirect('entrega:login_entrega')