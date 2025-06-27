from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from .models import Animal, Perro, Gato, Exotico, Propietario, Cita
from .form import *
from django.forms import modelformset_factory

def inicio (request):
    animales = Animal.objects.all()
    return render(request, 'inicio.html',{"animales":animales})


def cargar_animales(request):
    propietario_id = request.GET.get('propietario')
    animales = Animal.objects.filter(propietario_id=propietario_id).values('id', 'nombre_animal')
    return JsonResponse(list(animales), safe=False)

def AgendarCitas(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            # Aquí puedes agregar lógica adicional, como asignar el usuario
            # cita.usuario = request.user
            cita.save()
            messages.success(request, '¡Cita agendada exitosamente! Te contactaremos pronto para confirmar.')
            return redirect('inicio')  # Redirigir a la página principal
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CitaForm()
    
    return render(request, 'agendar_cita.html', {'form': form})

def agregar_propietario(request):
    if request.method == 'POST':
        propietario_form = PropietarioForm(request.POST)
        animal_form = AnimalForm(request.POST)
        tipo = request.POST.get("tipo_animal")

        perro_form = PerroForm(request.POST, prefix="perro")
        gato_form = GatoForm(request.POST, prefix="gato")
        exotico_form = ExoticoForm(request.POST, prefix="exotico")

        if propietario_form.is_valid() and animal_form.is_valid():
            propietario = propietario_form.save()
            animal_base = animal_form.save(commit=False)
            animal_base.propietario = propietario
            animal_base.save()  # Guardamos primero el Animal base


            if tipo == "perro" and perro_form.is_valid():
                perro = Perro(
                    id=animal_base.id,
                    nombre_animal=animal_base.nombre_animal,
                    especie=animal_base.especie,
                    edad=animal_base.edad,
                    fecha_ingreso=animal_base.fecha_ingreso,
                    propietario=animal_base.propietario,
                    tamanio=perro_form.cleaned_data["tamanio"],
                    raza=perro_form.cleaned_data["raza"],
                )
                perro.save()

            elif tipo == "gato" and gato_form.is_valid():
                gato = Gato(
                    id=animal_base.id,
                    nombre_animal=animal_base.nombre_animal,
                    especie=animal_base.especie,
                    edad=animal_base.edad,
                    fecha_ingreso=animal_base.fecha_ingreso,
                    propietario=animal_base.propietario,
                    color=gato_form.cleaned_data["color"],
                    raza=gato_form.cleaned_data["raza"],
                )
                gato.save()

            elif tipo == "exotico" and exotico_form.is_valid():
                exotico = Exotico(
                    id=animal_base.id,
                    nombre_animal=animal_base.nombre_animal,
                    especie=animal_base.especie,
                    edad=animal_base.edad,
                    fecha_ingreso=animal_base.fecha_ingreso,
                    propietario=animal_base.propietario,
                    tipo=exotico_form.cleaned_data["tipo"],
                    habitat=exotico_form.cleaned_data["habitat"],
                )
                exotico.save()

            else:
                messages.error(request, "Formulario del tipo de animal inválido.")
                return render(request, "propietario_form.html", {
                    'form': propietario_form,
                    'animal_form': animal_form,
                    'perro_form': perro_form,
                    'gato_form': gato_form,
                    'exotico_form': exotico_form,
                })

            messages.success(request, "Propietario y animal registrados correctamente.")
            return redirect('propietarios_lista')

        else:
            messages.error(request, "Corrige los errores en el formulario.")

    else:
        propietario_form = PropietarioForm()
        animal_form = AnimalForm()
        perro_form = PerroForm(prefix="perro")
        gato_form = GatoForm(prefix="gato")
        exotico_form = ExoticoForm(prefix="exotico")

    return render(request, "propietario_form.html", {
        'form': propietario_form,
        'animal_form': animal_form,
        'perro_form': perro_form,
        'gato_form': gato_form,
        'exotico_form': exotico_form,
    })

def lista_propietarios(request):
    """Vista para listar todos los propietarios"""
    propietarios = Propietario.objects.all().order_by('nombre')
    return render(request, 'propietarios_lista.html', {
        'propietarios': propietarios
    })


def editar_propietario(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)
    form = PropietarioForm(instance=propietario)
    formset = AnimalFormSet(queryset=Animal.objects.filter(propietario=propietario))

    perro_forms = []
    gato_forms = []
    exotico_forms = []

    for animal in formset.forms:
        if animal.instance.pk:
            try:
                perro = Perro.objects.get(pk=animal.instance.pk)
                perro_forms.append(PerroForm(instance=perro, prefix=f"perro_{animal.instance.id}"))
            except Perro.DoesNotExist:
                perro_forms.append(None)
            try:
                gato = Gato.objects.get(pk=animal.instance.pk)
                gato_forms.append(GatoForm(instance=gato, prefix=f"gato_{animal.instance.id}"))
            except Gato.DoesNotExist:
                gato_forms.append(None)
            try:
                exotico = Exotico.objects.get(pk=animal.instance.pk)
                exotico_forms.append(ExoticoForm(instance=exotico, prefix=f"exotico_{animal.instance.id}"))
            except Exotico.DoesNotExist:
                exotico_forms.append(None)
        else:
            perro_forms.append(None)
            gato_forms.append(None)
            exotico_forms.append(None)

    animales_con_forms = zip(formset.forms, perro_forms, gato_forms, exotico_forms)

    return render(request, "propietario_editar.html", {
        "form": form,
        "formset": formset,
        "animales_con_forms": animales_con_forms,
        "propietario": propietario,
    })

    return render(request, "propietario_editar.html", {
        "form": form,
        "formset": formset,
        "perro_forms": perro_forms,
        "gato_forms": gato_forms,
        "exotico_forms": exotico_forms,
        "propietario": propietario,
    })

def eliminar_propietario(request, propietario_id):
    """Vista para eliminar un propietario"""
    propietario = get_object_or_404(Propietario, id=propietario_id)
    
    if request.method == 'POST':
        nombre_propietario = propietario.nombre
        propietario.delete()
        messages.success(
            request, 
            f'Propietario {nombre_propietario} eliminado exitosamente.'
        )
        return redirect('propietarios_lista')
    
    return render(request, 'propietario_eliminar.html', {
        'propietario': propietario
    })


def historial_citas(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    citas = Cita.objects.filter(animal=animal).order_by('-fecha', '-hora')
    
    return render(request, 'historial.html', {
        'animal': animal,
        'citas': citas
    })