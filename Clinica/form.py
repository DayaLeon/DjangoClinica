from django import forms
from .models import *
from django.forms import modelformset_factory
import re

class CitaForm(forms.ModelForm):
    propietario = forms.ModelChoiceField(
        queryset=Propietario.objects.all(),
        required=True,
        label="Propietario",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors focus:outline-none',
            'id': 'id_propietario'
        })
    )

    class Meta:
        model = Cita
        fields = ['propietario', 'animal', 'fecha', 'hora', 'motivo']
        widgets = {
            'animal': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors focus:outline-none',
                'placeholder': 'Selecciona tu mascota',
                'id': 'id_animal'
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors focus:outline-none'
            }),
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors focus:outline-none'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors resize-none focus:outline-none',
                'rows': 4,
                'placeholder': 'Describe el motivo de la consulta...'
            }),
        }
        labels = {
            'animal': 'Mascota',
            'fecha': 'Fecha de la Cita',
            'hora': 'Hora Preferida',
            'motivo': 'Motivo de la Consulta'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicialmente, el queryset de animales está vacío
        self.fields['animal'].queryset = Animal.objects.none()

        # Si se está enviando el formulario con un propietario seleccionado
        if 'propietario' in self.data:
            try:
                propietario_id = int(self.data.get('propietario'))
                self.fields['animal'].queryset = Animal.objects.filter(propietario_id=propietario_id)
            except (ValueError, TypeError):
                pass
        # Si estamos editando una cita existente con un animal ya vinculado
        elif self.instance.pk and self.instance.animal:
            self.fields['animal'].queryset = Animal.objects.filter(propietario=self.instance.animal.propietario)

class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = ['nombre', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ingresa el nombre completo'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ej: +1 234 567 8900',
                'pattern': '[0-9+\-\s$$$$]+',
                'title': 'Solo números, espacios, guiones, paréntesis y signo +'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Calle, número, colonia, ciudad'
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'telefono': 'Número de Teléfono',
            'direccion': 'Dirección Completa'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS adicionales y hacer campos requeridos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': field.widget.attrs.get('class', '') + ' focus:outline-none'
            })
            field.required = True

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
            # Validar longitud mínima
            if len(nombre.strip()) < 2:
                raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        return nombre.title() if nombre else nombre

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Remover espacios y caracteres especiales para validación
            telefono_limpio = re.sub(r'[^\d]', '', telefono)
            if len(telefono_limpio) < 10:
                raise forms.ValidationError('El teléfono debe tener al menos 10 dígitos.')
            if len(telefono_limpio) > 15:
                raise forms.ValidationError('El teléfono no puede tener más de 15 dígitos.')
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if direccion:
            if len(direccion.strip()) < 10:
                raise forms.ValidationError('La dirección debe ser más específica (mínimo 10 caracteres).')
        return direccion.title() if direccion else direccion
    

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nombre_animal', 'especie', 'edad', 'fecha_ingreso']
        widgets = {
            'nombre_animal': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Nombre del animal'
            }),
            'especie': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ej: Perro, Gato, Ave...'
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Edad aproximada en años',
                'min': 0,
                'max': 100
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors'
            }),
        }
        labels = {
            'nombre_animal': 'Nombre del Animal',
            'especie': 'Especie',
            'edad': 'Edad (en años)',
            'fecha_ingreso': 'Fecha de Ingreso'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': field.widget.attrs.get('class', '') + ' focus:outline-none'
            })
            field.required = True

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
            if len(nombre.strip()) < 2:
                raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        return nombre.title() if nombre else nombre

    def clean_especie(self):
        especie = self.cleaned_data.get('especie')
        if especie:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', especie):
                raise forms.ValidationError('La especie solo puede contener letras y espacios.')
            if len(especie.strip()) < 3:
                raise forms.ValidationError('La especie debe tener al menos 3 caracteres.')
        return especie.title() if especie else especie

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is not None and (edad < 0 or edad > 100):
            raise forms.ValidationError('La edad debe estar entre 0 y 100 años.')
        return edad
    

class PerroForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ['tamanio', 'raza']
        widgets = {
            'tamanio': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Pequeño, Mediano, Grande'
            }),
            'raza': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ej: Labrador, Bulldog, etc.'
            }),
        }
        labels = {
            'tamanio': 'Tamaño',
            'raza': 'Raza'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' focus:outline-none'})
            field.required = True


class GatoForm(forms.ModelForm):
    class Meta:
        model = Gato
        fields = ['color', 'raza']
        widgets = {
            'color': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ej: Blanco, Atigrado, Negro'
            }),
            'raza': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ej: Persa, Siamés, etc.'
            }),
        }
        labels = {
            'color': 'Color del Gato',
            'raza': 'Raza'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': field.widget.attrs.get('class', '') + ' focus:outline-none'
            })
            field.required = True

    def clean_color(self):
        color = self.cleaned_data.get('color')
        if color:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', color):
                raise forms.ValidationError('El color solo puede contener letras y espacios.')
            if len(color.strip()) < 3:
                raise forms.ValidationError('El color debe tener al menos 3 caracteres.')
        return color.title() if color else color

    def clean_raza(self):
        raza = self.cleaned_data.get('raza')
        if raza:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', raza):
                raise forms.ValidationError('La raza solo puede contener letras y espacios.')
            if len(raza.strip()) < 3:
                raise forms.ValidationError('La raza debe tener al menos 3 caracteres.')
        return raza.title() if raza else raza


class ExoticoForm(forms.ModelForm):
    class Meta:
        model = Exotico
        fields = ['tipo', 'habitat']
        widgets = {
            'tipo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ej: Reptil, Ave, Roedor...'
            }),
            'habitat': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors',
                'placeholder': 'Ej: Terrario húmedo, jaula grande con ramas...',
                'rows': 3
            }),
        }
        labels = {
            'tipo': 'Tipo de Animal Exótico',
            'habitat': 'Descripción del Hábitat'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': field.widget.attrs.get('class', '') + ' focus:outline-none'
            })
            field.required = True

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if tipo:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', tipo):
                raise forms.ValidationError('El tipo solo puede contener letras y espacios.')
            if len(tipo.strip()) < 3:
                raise forms.ValidationError('El tipo debe tener al menos 3 caracteres.')
        return tipo.title() if tipo else tipo

    def clean_habitat(self):
        habitat = self.cleaned_data.get('habitat')
        if habitat:
            if len(habitat.strip()) < 10:
                raise forms.ValidationError('El hábitat debe tener al menos 10 caracteres.')
        return habitat.capitalize() if habitat else habitat



AnimalFormSet = modelformset_factory(
    Animal,
    form=AnimalForm,  # o simplemente 'form=None' si usas el modelo directo
    extra=0,
    can_delete=False,
)