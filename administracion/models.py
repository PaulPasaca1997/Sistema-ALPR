from pickle import NONE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.


class Rol (models.Model):
    roles = models.CharField(max_length=25)

    # PARA MOSTRAR LOS NOMBRES EN LA TABLA, SINO SE PONE SE MUESTRAN COMO OBJETOS
    def __str__(self):
        return self.roles


class Usuario(models.Model):
    usuario= models.ForeignKey(User,on_delete=models.CASCADE)
    cedula = models.PositiveIntegerField()
    
   
class Placa(models.Model):
    placa = models.CharField(max_length=7)
    marca = models.CharField(max_length=7)
    
    

    
 # https://www.youtube.com/watch?v=N6jzspc2kds&ab_channel=CodAffection
 # https://bootsnipp.com/tags/login
# limpiar base de datos---- para las migraciones---- python manage.py flush 
# luego de eso eliminar todos archivos dentro de migrations y borrar bd en pdadmin 


