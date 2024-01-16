from django.shortcuts import render
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import requests
import json
import pathlib
load_dotenv()
from .models import Feedback
from rest_framework import generics
from .models import Feedback
from .serializers import FeedbackSerializer


def index(request):
    return render(request, 'pesquisa_satisfacao/index.html')


from datetime import datetime

def nps(request, pedido, data_pedido):
    if request.method == 'POST':
        existing_feedback = Feedback.objects.filter(pedido=pedido).first()
        if existing_feedback is not None:
            return render(request, 'pesquisa_satisfacao/erro.html')
        else:
            rating = request.POST.get('rating')
            email = request.POST.get('email')
            selected_options = request.POST.getlist('options[]')
            indicacao = request.POST.get('indicacao')
     
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            loja_id = pedido.split('-')[0]

            
            feedback = Feedback(
                rating=rating,
                selected_options=selected_options,
                indicacao=indicacao,
                email=email,
                pedido=pedido,
                data_pedido=datetime.strptime(data_pedido, "%Y-%m-%d").date(),  
                loja_id=loja_id,
                timestamp=timestamp
            )
            feedback.save()
            status_code, response_data = send_to_powerbi(rating, selected_options, indicacao, pedido, timestamp, feedback.id, data_pedido, loja_id)
            return render(request, 'pesquisa_satisfacao/sucesso.html')

    return render(request, 'pesquisa_satisfacao/form.html')
class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

def send_to_powerbi(rating, selected_options, indicacao, pedido, timestamp, id, data_pedido, loja_id):
    endpoint = "https://api.powerbi.com/beta/27cc7714-ecb3-407d-8115-da53f624c6da/datasets/97ce61bc-7baa-4ea0-9da9-fd828ca80001/rows?experience=power-bi&key=VMwO9O6yV3fKBiANDusDxbRUXsdQ6WyssPST1BVEx52KadC0KtK5tdSf9hXpJuR9D3%2FbuXvJb6NvY4EXSIpJ3Q%3D%3D"
    
 
    payloads = []
    for option in selected_options:
        payloads.append({
            "rating": rating,
            "selected_options": option,
            "indicacao": indicacao,
            "pedido": pedido,
            "timestamp": timestamp,
            "data_pedido": data_pedido,
            "id": id,
            "loja_id": loja_id,

        })

    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(endpoint, data=json.dumps(payloads), headers=headers)
    if response.text:
        return response.status_code, response.json()
    else:
        return response.status_code, None
    

def envio(request):
    if request.method == 'GET':
        return render(request, 'pesquisa_satisfacao/email.html')
    if request.method == 'POST':
        
        file = request.FILES['file']
        df = pd.read_excel(file)

  
        smtp_server = 'smtp.condor.com.br'
        smtp_port = 587
        smtp_username = 'sac.cec'
        smtp_password = 'PXGf@3PU'

        datas_pedido = df['data'].tolist()
        emails = df['Email']  
        nomes = df['nome'] 
        pedidos = df['pedido'] 
        pedidos = df['pedido'].astype(str).str.rstrip('.0').tolist()
        data_pedido = df['data']
        CAMINHO_HTML = 'base_templates/global/arte1.html'


        with open(CAMINHO_HTML, 'r') as arquivo:
            texto_arquivo = arquivo.read()

        for email, nome, pedido, data in zip(emails, nomes, pedidos, data_pedido):
            formatted_data = data.strftime('%Y-%m-%d')
            remetente = 'Condor em Casa <sac.cec>'
            destinatario = email


            #texto_email = texto_arquivo.replace('{pedido}', str(pedido))
            texto_email = (texto_arquivo.replace('{pedido}', str(pedido))
                           .replace('{data_pedido}', str(formatted_data)))

            print(email, data_pedido)
            mime_multipart = MIMEMultipart()
            mime_multipart['from'] = remetente
            mime_multipart['to'] = destinatario
            mime_multipart['subject'] = 'Pesquisa Satisfação Condor em Casa'

            corpo_email = MIMEText(texto_email, 'html', 'utf-8')
            mime_multipart.attach(corpo_email)

            # Envia o e-mail
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                
                server.ehlo()
                server.login(smtp_username, smtp_password)
                server.send_message(mime_multipart)
                print(f'E-mail enviado para {email} com sucesso!')

        return render(request, 'pesquisa_satisfacao/email.html')
