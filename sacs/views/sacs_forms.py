from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from sacs.forms import ContactForm
from django.urls import reverse
from sacs.models import Contact
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from django.contrib.auth.models import Group


load_dotenv()
@login_required(login_url='sacs:login')
def create(request):
    owner = request.user
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, initial={'user': owner}) #
        if form.is_valid():
            contact = form.save(commit=False)
            contact.created_date = timezone.now()#.strftime("%Y-%m-%d %H:%M:%S")
            if not contact.owner:  # Verificar se o contato já tem um owner definido
                #  contact.owner = owner # Definir o owner do contato somente se não estiver definido
                
                group = contact.group 
                users = group.user_set.all() 
                contact.owner = users.first() 
                print(f'Owner - {contact.owner}')
            contact.save()
            
            email_email2(contact)  
            return redirect('contact:index')
    else:
        if owner.is_superuser:
            form = ContactForm(initial={'user': owner})#initial={'user': owner}
        else:
            form = ContactForm(initial={'user': owner})#initial={'user': owner}
            # form.fields['owner'].queryset = User.objects.filter(id=owner.id)
            form.fields['group'].queryset = request.user.groups.all()


    context = {
        'form': form,
        'form_action': form_action,
    }
    return render(request, 'sacs/create.html', context)




@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)

    form_action = reverse('contact:update', args=(contact_id,))

    if not request.user.is_superuser:
        form = ContactForm(request.POST or None, request.FILES or None, instance=contact, user=request.user)
        for field_name, field in form.fields.items():
            if field_name != 'description_store':
                field.widget.attrs['disabled'] = 'disabled'
                
                
    else:
        form = ContactForm(request.POST or None, request.FILES or None, instance=contact)

    form.fields['owner'].queryset = User.objects.filter(id=request.user.id) if not request.user.is_superuser else User.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            contact = form.save()
            return redirect('contact:contact', contact_id=contact.pk)
    
    context = {
        'form': form,
        'form_action': form_action,
    }

    return render(request, 'sacs/create.html', context)


@login_required(login_url='sacs:login')
def delete(request, contact_id):
    owner = request.user
    if owner.username == 'admin':
        contact = get_object_or_404(
            Contact, pk=contact_id, show=True #, owner=request.user

        )
        confirmation = request.POST.get('confirmation', 'no')
        if confirmation == 'yes':
            contact.delete()

            return redirect('contact:index')
        return render(
            request,
            'sacs/contact.html',
            {
                'contact': contact,
                'confirmation': confirmation,   

            }
        )
    else:
        messages.info(request, 'Sem permissão!')
        return redirect('contact:index')

def email_email2(contact):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    # smtp_username = os.getenv('FROM_EMAIL', '')
    # smtp_password = os.getenv('EMAIL_PASSWORD', '')
    smtp_username = 'saccec.condor@gmail.com'
    smtp_password = "bebg yxwi msdt ftqx"
    pedido = contact.last_name
    owner = contact.owner
    categoria = contact.category.name
    link = contact.pk
    with open('base_templates/global/email.html', 'r', encoding='utf-8') as file:
        template = file.read()
    template = template.replace('{{owner}}', str(owner))
    template = template.replace('{{categoria}}', categoria)
    template = template.replace('{{link}}', str(link))
    template = template.replace('{{pedido}}', pedido)
    remetente = 'saccec.condor@gmail.com'
    destinatario = owner.email
    print(f'Email enviado para {destinatario} - Owner - {owner}')
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