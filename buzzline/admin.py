from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Beep

# REMOVENDO A SEÇÃO GROUPS DE /ADMIN
admin.site.unregister(Group)

# JUNTANDO INFORMAÇÕES PERFIL E USUARIO
class ProfileInline(admin.StackedInline): 
    model = Profile
    
# EXTEND USER MODEL
class UserAdmin(admin.ModelAdmin):
    model = User
    # JUST DISPLAY USERNAME FIELDS ON ADMIN PAGE
    fields = ["username"]
    inlines = [ProfileInline]


# REMOVENDO USER INICIAL
admin.site.unregister(User)

# REGISTRANDO USER AND PROFILE
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Registrar os Beeps
admin.site.register(Beep)

