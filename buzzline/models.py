from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Criando o Modelo Beep

class Beep(models.Model):
    user = models.ForeignKey(User, related_name="beeps", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.user}"
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )

# CRIANDO MODELO PERFIL DE USUARIO
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # UM USUARIO TERÁ 1 PERFIL, LOGO 1 PERFIL TERÁ APENAS 1 USUARIO
    follows = models.ManyToManyField("self", # UM PERFIL PODE SEGUIR MUITOS PERFIS
        related_name="followed_by", # QUEM SEGUE ESSE PERFIL
        symmetrical=False, # A PESSOA QUE SEGUE O OUTRO NÃO PRECISA SEGUIR DE VOLTA
        blank=True #NÃO É OBRIGADO A SEGUIR ALGUEM ESSE VALOR PODE SER VAZIO
        ) 
    
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/')
    def __str__(self):
        return self.user.username

# Criar Perfil Quando Um novo usuario se cadastrar
# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Os usuários tem que seguir eles mesmos quando criados
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)