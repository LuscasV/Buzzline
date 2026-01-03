from django import forms
from .models import Beep, Profile, Comment
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

# Profile Extras formulario
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Foto de Perfil")
    
    profile_bio = forms.CharField(label="Bio do perfil", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio do Perfil', 'style': 'resize: none;'}))
    homepage_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link do Website'}))
    facebook_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link do Facebook'}))
    instagram_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link do Instagram'}))
    linkedin_link = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link do Linkedin'}))
    
    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link')

class BeepForm(forms.ModelForm):
    body = forms.CharField(required=True,
    widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Digite seu Beep!",
            "class":"form-control",
            'style': 'resize: none;'
            }
            ),
            label="",                       
        )
    
    class Meta:
        model = Beep
        exclude = ("user", "likes",)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Obrigatório. 150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'
            '</small></span>'
        )

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Sua senha não deve ser muito semelhante às suas outras informações pessoais.</li>'
            '<li>Sua senha deve conter pelo menos 8 caracteres.</li>'
            '<li>Sua senha não deve ser uma senha comumente usada.</li>'
            '<li>Sua senha não deve ser totalmente numérica.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Digite a mesma senha de antes para verificação.'
            '</small></span>'
        )

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome'
        })
    )

    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Obrigatório. 150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'
            '</small></span>'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        user_id = self.instance.id

        if User.objects.exclude(id=user_id).filter(username=username).exists():
            raise forms.ValidationError("Já existe um usuário com esse nome.")

        return username

class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Senha atual",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )

    new_password1 = forms.CharField(
        label="Nova senha",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        }),
        help_text=(
            '<ul class="form-text text-muted small">'
            '<li>Sua senha não deve ser muito semelhante às suas outras informações pessoais.</li>'
            '<li>Sua senha deve conter pelo menos 8 caracteres.</li>'
            '<li>Sua senha não deve ser uma senha comumente usada.</li>'
            '<li>Sua senha não deve ser totalmente numérica.</li>'
            '</ul>'
        )
    )

    new_password2 = forms.CharField(
        label="Confirmar nova senha",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        }),
        help_text=(
            '<span class="form-text text-muted"><small>'
            'Digite a mesma senha de antes para verificação.'
            '</small></span>'
        )
    )
    

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escreva um comentário...',
            'rows': 3,
            'style': 'resize: none;'
        })
    )

    class Meta:
        model = Comment
        fields = ('body',)
