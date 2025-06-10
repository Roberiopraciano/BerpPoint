from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from random import randint

class Employee(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    photo = models.ImageField(upload_to='photo/')
    cpf = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        seq = self.name + '_FUNC' + str(randint(1000000, 9999999))
        self.slug = slugify(seq)
        super().save(*args, **kwargs)


class FaceCollection(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_collection')
    image = models.ImageField(upload_to='roi/')

    class Meta:
        verbose_name = 'Coleta de Face'
        verbose_name_plural = 'Coleta de Faces'


class Training(models.Model):
    model = models.FileField(upload_to='training/')

    class Meta:
        verbose_name = 'Treinamento'
        verbose_name_plural = 'Treinamentos'

    def __str__(self):
        return 'Classificadores (frontalface)'
    
    def clean(self):
        model = self.__class__

        if model.objects.exclude(id=self.id).exists():
            raise ValidationError('Só pode haver um arquivo salvo.')
        
class EmployeeRegistration(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    class Meta:
        verbose_name = 'Registro de Funcionário'
        verbose_name_plural = 'Registro de Funcionários'

    def __str__(self):
        return f"{self.employee.name} - {self.datetime}"