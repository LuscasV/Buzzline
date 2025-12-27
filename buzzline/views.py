from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Beep
from .forms import BeepForm, SignUpForm, ProfilePicForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        form = BeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                beep = form.save(commit=False)
                beep.user = request.user
                beep.save()
                messages.success(request, ("Seu Beep foi postado!"))
                return redirect('home')

        beeps = Beep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"beeps": beeps, "form": form,})
    else:
        beeps = Beep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"beeps": beeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles })
    else:
        messages.success(request, ("Você precisa estar logado para ver essa página"))
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        # Pegar o perfil pra parar de seguir
        profile = Profile.objects.get(user_id=pk)
        # Deixar de seguir o usuario
        request.user.profile.follows.remove(profile)
        # Salvar nosso perfil
        request.user.profile.save()

        #Mensagem de retorno!
        messages.success(request, (f"Você deixou de seguir {profile.user.username} "))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("Você precisa estar logado para acessar essa página!"))
        return redirect('home')

def follow(request, pk):
    if request.user.is_authenticated:
        # Pegar o perfil pra parar de seguir
        profile = Profile.objects.get(user_id=pk)
        # Deixar de seguir o usuario
        request.user.profile.follows.add(profile)
        # Salvar nosso perfil
        request.user.profile.save()

        #Mensagem de retorno!
        messages.success(request, (f"Você Seguiu {profile.user.username} "))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("Você precisa estar logado para acessar essa página!"))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        beeps = Beep.objects.filter(user_id=pk).order_by("-created_at")

        # POST FORM LOGICA
        if request.method == "POST":
            # PEGAR O USUARIO 
            current_user_profile = request.user.profile
            # PEGAR OS DADOS DO FORM
            action = request.POST['follow']
            # Decidir seguir ou deixar de seguir
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Salvar o Perfil
            current_user_profile.save()
        return render(request, "profile.html", {"profile":profile, "beeps":beeps})
    else:
        messages.success(request, ("Você precisa estar logado para ver essa página"))
        return redirect('home')

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles":profiles })
        else:
            messages.success(request, ("Essa não é a página do seu perfil..."))
            return redirect('home')

    else:
        messages.success(request, ("Você precisa estar logado para ver essa página"))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles":profiles })
        else:
            messages.success(request, ("Essa não é a página do seu perfil..."))
            return redirect('follows')

    else:
        messages.success(request, ("Você precisa estar logado para ver essa página"))
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login efetuado!"))
            return redirect('home')
        else:
            messages.success(request, ("Ocorreu um erro ao tentar fazer o login, por favor tente novamente"))
            return redirect('login')

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Login finalizado!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Usuário registrado com sucesso! Bem-vindo!"))
            return redirect('home')
    return render(request, "register.html", {'form':form})


# def update_user(request):
#     # lógica para só ser possível acessar o update_user se estiver logado
#     if request.user.is_authenticated:
#         current_user = User.objects.get(id=request.user.id)
#         profile_user = Profile.objects.get(user__id=request.user.id)
#         user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
#         profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             login(request, current_user)
#             messages.success(request, ("Perfil editado com sucesso!"))
#             return redirect('home')
#         return render(request, "update_user.html", {'user_form': user_form, 'profile_form':profile_form})
#     else:
#         messages.success(request, ("Você precisa estar logado para acessar essa página!"))
#         return redirect('home')
    
@login_required # CORREÇÃO DO UPDATE USER #
def update_user(request):
    current_user = request.user
    profile_user = Profile.objects.get(user=current_user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=current_user)
        profile_form = ProfilePicForm(
            request.POST, request.FILES, instance=profile_user
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil editado com sucesso!")
            return redirect('profile', current_user.id)
    else:
        user_form = UpdateUserForm(instance=current_user)
        profile_form = ProfilePicForm(instance=profile_user)

    return render(request, "update_user.html", {
        'user_form': user_form,
        'profile_form': profile_form
    })


def beep_like(request, pk):
    if request.user.is_authenticated:
        beep = get_object_or_404(Beep, id=pk)
        if beep.likes.filter(id=request.user.id):
            beep.likes.remove(request.user)
        else:
            beep.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ("Você precisa estar logado para acessar essa página!"))
        return redirect('home')


def beep_show(request, pk):
    beep = get_object_or_404(Beep, id=pk)
    if beep:
        return render(request, 'show_beep.html', {"beep":beep })
    else:
        messages.success(request, ("Esse Beep não existe!"))
        return redirect('home')

def delete_beep(request, pk):
    if request.user.is_authenticated:
        beep = get_object_or_404(Beep, id=pk)
        # Check para ver se o usuário é dono do beep
        if request.user.username == beep.user.username:
            # Deletar o Beep!
            beep.delete()
            messages.success(request, ("O Beep foi deletado com sucesso!"))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, ("Esse Beep não pertence a você!"))
            return redirect('home')
    else:
        messages.success(request, ("Por favor, faça o login para continuar..."))
        return redirect(request.META.get('HTTP_REFERER'))

def edit_beep(request, pk):
    if request.user.is_authenticated:
        # Capturando o Beep
        beep = get_object_or_404(Beep, id=pk)
        # Check para ver se o usuário é dono do beep
        if request.user.username == beep.user.username:
            
            form = BeepForm(request.POST or None, instance=beep)
            if request.method == "POST":
                if form.is_valid():
                    beep = form.save(commit=False)
                    beep.user = request.user
                    beep.save()
                    messages.success(request, ("Seu Beep foi editado!"))
                    return redirect('home')
            else:
                return render(request, "edit_beep.html", {'form': form, 'beep':beep })
            
        else:
            messages.success(request, ("Esse Beep não pertence a você!"))
            return redirect('home')
    else:
        messages.success(request, ("Por favor, faça o login para continuar..."))
        return redirect('home')
    
def search(request):
    if request.method == "POST":
        # CAPTURANDO O CAMPO INPU DO FORMULARIO
        search = request.POST['search']
        # PROCURAR O BANCO DE DADOS
        searched = Beep.objects.filter(body__contains = search)
        return render(request, 'search.html', {'search':search, 'searched': searched})
    else:
        return render(request, 'search.html', {})

def search_user(request):
    if request.method == "POST":
        # CAPTURANDO O CAMPO INPU DO FORMULARIO
        search = request.POST['search']
        # PROCURAR O BANCO DE DADOS
        searched = User.objects.filter(username__contains = search)
        
        return render(request, 'search_user.html', {'search':search, 'searched': searched})
    else:
        return render(request, 'search_user.html', {})