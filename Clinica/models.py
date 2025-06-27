from django.db import models

class Propietario(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class Animal(models.Model):
    nombre_animal = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    edad = models.IntegerField()
    fecha_ingreso = models.DateField()
    propietario = models.ForeignKey('Propietario', on_delete=models.CASCADE, related_name='animales', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"

class Perro(Animal):
    tamanio = models.CharField(max_length=20)  # Pequeño, Mediano, Grande
    raza = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.nombre} - {self.tamanio}"

class Gato(Animal):
    color = models.CharField(max_length=30)
    raza = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.nombre} - {self.color}"
    
class Exotico(Animal):
    tipo = models.CharField(max_length=50)  # Ejemplo: Reptil, Ave, Roedor
    habitat = models.CharField(max_length=100)  # Descripción del hábitat
    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
    
class Cita(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()

    def __str__(self):
        return f"Cita para {self.animal.nombre} el {self.fecha} a las {self.hora}"
    

