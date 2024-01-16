from django.shortcuts import render, get_object_or_404, redirect
from sacs import views
from sacs.models import Contact
from django.db.models import Q
from django.core.paginator import Paginator
from sacs.models import models
from sacs.models import ContactLog
from sacs.forms import ContactForm
from django.utils import timezone
from django.contrib import messages
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging
logger = logging.getLogger(__name__)
from user_agents import parse


def index(request): 
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    is_mobile = user_agent.is_mobile
    owner = request.user

    if owner.is_superuser:
        contacts = Contact.objects.filter(show=True).order_by('-status')
         
    else:   
        contacts = Contact.objects.filter(group__in=request.user.groups.all(), show=True).order_by('-status')
    
    
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Sacs - ',
        'is_mobile': is_mobile,
          
    }
    return render(request, 'sacs/index.html', context)


def iniciar(request, contact_id):
    owner = request.user

    if owner.is_superuser:
        single_contact = get_object_or_404(Contact, pk=contact_id, show=True)
    else:
        single_contact = get_object_or_404(Contact, pk=contact_id, show=True, group__in=request.user.groups.all())

    if request.method == 'GET' and single_contact.status != 'concluido':
        single_contact.status = "Pendente"
        single_contact.inicio_atendimento = timezone.now()#.strftime("%Y-%m-%d %H:%M:%S")
        single_contact.save()
        ContactLog.objects.create(contact=single_contact, user=owner, action="Iniciou o atendimento")

    site_title = f'{single_contact.first_name} {single_contact.last_name} - '

    context = {
        'contact': single_contact,
        'site_title': site_title,
    }

    return render(request, 'sacs/iniciar.html', context)


def contact(request, contact_id):
    user_name = request.user.get_username()
    stamp = timezone.now()
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True)
    owner = request.user
    if owner.is_superuser:
        single_contact = get_object_or_404(Contact, pk=contact_id, show=True) 
    else:
        single_contact = get_object_or_404(Contact, pk=contact_id, show=True, group__in=request.user.groups.all())
    if request.method == 'POST' and single_contact.status != 'Concluído':
        single_contact.status = "Em atendimento"
        single_contact.save()
    if request.method == 'POST' and 'obs' in request.POST:
        observacao = request.POST.get('obs')
        single_contact.description_store = observacao
        single_contact.save()
        ContactLog.objects.create(contact=single_contact, user=owner, action=f"Adicionou uma observação: {observacao}"  )
        contact_id = contact_id
        messages.success(request, 'Obrigado pelo retorno!')
    site_title = f'{single_contact.first_name} {single_contact.last_name} - '
    context = {
        'contact': single_contact,
        'site_title': site_title,
        'observacao': single_contact.description_store,
    }

    return render(request, 'sacs/contact.html', context)

def completed(request, contact_id):
    owner = request.user
    user_name = request.user.get_username()
    stamp = timezone.now()
    if owner.is_superuser:
        single_contact = get_object_or_404(Contact, pk=contact_id)
        if request.method == 'POST':
            single_contact.status = 'Concluído'
            single_contact.timestamp = timezone.now()#.strftime("%Y-%m-%d %H:%M:%S")
            single_contact.save()        
        context = {
            'contact': single_contact,
        }
        
        messages.success(request, 'SAC Concluído!')
        return redirect('contact:index')
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True, group__in=request.user.groups.all())
    if request.method == 'POST':
        single_contact.status = 'Concluído'
        single_contact.timestamp = timezone.now()#.strftime("%Y-%m-%d %H:%M:%S")
        single_contact.save()
        ContactLog.objects.create(contact=single_contact, user=owner, action="Concluiu")

        context = {
            'contact': single_contact,
        }
        messages.success(request, 'SAC Concluído!')
        email_completed(single_contact)
        return redirect('contact:index')
def search(request):
    owner = request.user
    if owner.is_superuser:
        search_value = request.GET.get('q', '').strip()
        if search_value == '':
            return redirect('contact:index')
        contacts = Contact.objects \
        .filter(show=True)\
        .filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(category__name__icontains=search_value) | 
                Q(pk__icontains=search_value) |
                Q(status__icontains=search_value) |
                Q(owner__username__icontains=search_value)                 
        ) \
        .order_by('-status')
        paginator = Paginator(contacts, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'site_title': 'Contatos - ', 
            'search_value': search_value,
        }
        return render(request, 
                    'sacs/index.html', 
                    context)
    search_value = request.GET.get('q', '').strip()
    if search_value == '':
            return redirect('contact:index')
    contacts = Contact.objects \
        .filter(
                Q(owner=owner) | Q(group__user=owner),
                show=True
                )\
        .filter(
                Q(created_date__icontains=search_value) |
                Q(category__name__icontains=search_value) |
                Q(pk__icontains=search_value) |
                Q(status__icontains=search_value) 
            )\
        .order_by('-status')\
        .distinct()
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
            'page_obj': page_obj,
            'site_title': 'Contatos - ', 
            'search_value': search_value,
        }
    return render(request, 
                    'sacs/index.html', 
                    context)
def search2(request):
    owner = request.user
    if request.method == 'POST':
        if owner.is_superuser:
            search_value = request.POST.get('status', '').strip()
            if not search_value:
                print('condicao', search_value)   
                return redirect('contact:index')
            contacts = Contact.objects \
            .filter(show=True)\
            .filter(
                    
                    Q(category__name__icontains=search_value) |  
                    Q(pk__icontains=search_value) |
                    Q(status__icontains=search_value) 
            ) \
            .order_by('-status')
            paginator = Paginator(contacts, 20)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            context = {
                'page_obj': page_obj,
                'site_title': 'Contatos - ', 
                'search_value': search_value,
            }
            
            return render(request, 
                        'sacs/index.html', 
                        context)
        search_value = request.POST.get('status', '').strip()
        if search_value == '':
            return redirect('contact:index')
        contacts = Contact.objects \
        .filter(
        Q(owner=owner) | Q(group__user=owner),
        show=True
        ) \
        .filter(
            Q(category__name__icontains=search_value) |  
            Q(pk__icontains=search_value) |
            Q(status__icontains=search_value) 
            ) \
        .order_by('-status') \
        .distinct()
        paginator = Paginator(contacts, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'site_title': 'Contatos - ', 
            'search_value': search_value,
            }
        return render(request, 
                'sacs/index.html', 
                        context)   
def email_completed(contact):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    # smtp_username = os.getenv('FROM_EMAIL', '')
    # smtp_password = os.getenv('EMAIL_PASSWORD', '')
    smtp_username = 'saccec.condor@gmail.com'
    smtp_password = "bebg yxwi msdt ftqx"
    pedido = contact.last_name
    owner = contact.owner
    obs_loja = contact.description_store
    with open('base_templates/global/email2.html', 'r', encoding='utf-8') as file:
        template = file.read()
    template = template.replace('{{owner}}', str(owner))
    template = template.replace('{{obs_loja}}', obs_loja)
    template = template.replace('{{pedido}}', pedido)
    remetente = 'saccec.condor@gmail.com'
    destinatario = remetente
    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = remetente
    mime_multipart['to'] = destinatario
    mime_multipart['subject'] = 'SAC - Condor em Casa'
    corpo_email = MIMEText(template, 'html', 'utf-8')
    mime_multipart.attach(corpo_email)
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(mime_multipart)