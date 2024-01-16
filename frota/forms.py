from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from . import models
from .models import Entrega, Insucesso
import re
from django.core.files.storage import FileSystemStorage



from django.core.files.storage import FileSystemStorage

class PictureForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['picture']

    def save(self, commit=True):
        # Chamando o método save original para obter o objeto, mas sem salvá-lo no banco de dados ainda
        instance = super(PictureForm, self).save(commit=False)
        
        if 'picture' in self.cleaned_data:
            myfile = self.cleaned_data['picture']
            
            # Formatar o nome da imagem diretamente no arquivo
            ext = myfile.name.split('.')[-1]
            myfile.name = f"{instance.numero_pedido}_{instance.group}.{ext}"
            
            if commit:
                instance.save()

        return instance



class InsucessoForm(forms.ModelForm):
    class Meta:
        model = Insucesso
        fields = ['img_insucesso']
class EntregaForm(forms.ModelForm):

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False

    )
   
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['owner'].queryset = User.objects.filter(id=user.id)
        elif user:
            self.fields['owner'].queryset = User.objects.all()

    class Meta():
       
        model = models.Entrega
       
        fields = ('first_name', 'numero_pedido', 'phone',
                    'email', 'data_ent', 'janela', 'description', 'endereco', 'bairro', 'category',
                    'owner', 'status', 'group',
        )
            

   
   
   
    
    
    def clean(self):
       
        cleaned_data = self.cleaned_data
        # first_name = cleaned_data.get('first_name')
        numero_pedido = cleaned_data.get('numero_pedido')
       
       
        if len(numero_pedido) < 2:
            msg = ValidationError(
                'Mínimo de 2 caracteres',
                code='invalid'
            )
            
            self.add_error('numero_pedido', msg)
        

        return super().clean()
    

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'Veio do add_error',
                    code='invalid'
                )
            )

        return first_name

    



class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        
    )


    class Meta:
        model = User
        fields = (

            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe esse email', code='invalid')
            )

        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )


    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user


    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()




    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                    )

            return email
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

            return password1