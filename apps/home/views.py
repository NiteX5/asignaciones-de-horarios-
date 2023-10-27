from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *




@login_required(login_url="/login/")
def index(request):
    context = {}
    current_user = User.objects.get(username=request.user)
    user_info_instance = user_info.objects.get(user=current_user)
    context = {'departament': user_info_instance.departament, 'segment': 'index'}
    if user_info_instance.departament == 'Secretaria':
        html_template = loader.get_template('home/asignacion.html')
        return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template('home/horarios-list.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        # tomamos los datos del usuario para administar los permisos a las vistas
        current_user = User.objects.get(username=request.user)
        user_info_instance = user_info.objects.get(user=current_user)
        context = {'departament': user_info_instance.departament, 'segment': 'index', 'form': 'form'}

        # indicamos la ruta de la vista que se va a cargar
        load_template = request.path.split('/')[-1]

        # se devuelve la vista de admin
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        # damos context y cargamos la vista
        context['segment'] = load_template
        
        
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    


# crud Cursos

@login_required(login_url="/login/")
def get_courses(request):
    courses = Course.objects.values()
    return JsonResponse({'data': list(courses)})

@login_required(login_url="/login/")
def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course', '').upper()

        # Verifica si el curso ya existe
        exist = Course.objects.filter(course=course_name).exists()
        if exist:
            return JsonResponse({'message': 'Curso ya existe'})

        new_course = Course(course=course_name)
        new_course.save()
        return JsonResponse({'message': 'Curso agregado exitosamente'})
    else:
        return JsonResponse({'message': 'error del sistema'})

@login_required(login_url="/login/")
def edit_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('id', '')
        course_name = request.POST.get('course', '').upper()
        course = Course.objects.get(pk=course_id)
        course.course = course_name
        course.save()
        return JsonResponse({'message': 'Curso editado exitosamente'})

@login_required(login_url="/login/")
def delete_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('id', '')
        course = Course.objects.get(pk=course_id)
        course.delete()
        return JsonResponse({'message': 'Curso eliminado exitosamente'})


# crud usuarios
@login_required(login_url="/login/")
def get_users(request):
    users = user_info.objects.select_related('user').values('id', 'first_name', 'last_name', 'phone_number', 'email', 'departament', 'user__username')
    return JsonResponse({'data': list(users)})



@login_required(login_url="/login/")
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')
        departament = request.POST.get('departament', '')
        user = User.objects.filter(username=username).exists()
        if user:
            return JsonResponse({'message': 'Usuario '+ username + ' ya existe'})
        user = User.objects.create_user(username=username, password=password)
        user_id = user.id
        user_info_obj = user_info.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            departament=departament,
            user_id=user_id  
        )
        
        return JsonResponse({'message': 'Usuario agregado exitosamente'})

@login_required(login_url="/login/")
def edit_user(request):
    if request.method == 'POST':
        user_id = int(request.POST.get('id', ''))
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')
        departament = request.POST.get('departament', '')

        uid = user_info.objects.get(id=user_id)

        user = User.objects.get(username=uid.user)
        user.username = username
        if password != '':
            user.set_password(password)
        user.save()
        user_info_obj = user_info.objects.get(id=user_id)
        user_info_obj.first_name = first_name
        user_info_obj.last_name = last_name
        user_info_obj.phone_number = phone_number
        user_info_obj.email = email
        user_info_obj.departament = departament
        user_info_obj.save()
        return JsonResponse({'message': 'Usuario editado exitosamente'})
    else:
        print('error')
        return JsonResponse({'message': 'error'})
    
    
@login_required(login_url="/login/")
def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('id', '')
        uid = user_info.objects.get(id=user_id)
        user_infos = user_info.objects.get(pk=user_id)
        user_infos.delete()
        user = User.objects.get(username=uid.user)
        user.delete()

        
        return JsonResponse({'message': 'Usuario eliminado exitosamente'})
    
# crud asignaturas

@login_required(login_url="/login/")
def get_subjects(request):
    subjects = Subjects.objects.values('id', 'subject', 'course__course', 'course__id', 'prefix')
    return JsonResponse({'data': list(subjects)})

@login_required(login_url="/login/")
def add_subjects(request):
    if request.method == 'POST':
        asignatura = request.POST.get('asignatura', '')
        nivel = int(request.POST.get('nivel', ''))
        prefijo = request.POST.get('prefijo', '').upper()
        
        # obtenemos el objeto curso atravez de la clave primaria para poder hacer una relacion Many-to-one
        # ? Documentacion: https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/
        course = Course.objects.get(pk=nivel)
        
        # Verifica si la asignatura ya existe
        exist = Subjects.objects.filter(subject=asignatura, course=course).exists()
        if exist:
            return JsonResponse({'message': 'Asignatura ya existe'})
        else:
            new_subject = Subjects(subject=asignatura, prefix=prefijo, course=course)
            new_subject.save()
            return JsonResponse({'message': 'Asignatura agregada exitosamente'})
    else:
        return JsonResponse({'message': 'error'})

@login_required(login_url="/login/")
def edit_subjects(request):
    if request.method == 'POST':
        subject_id = request.POST.get('id', '')
        asignatura = request.POST.get('asignatura', '')
        nivel = int(request.POST.get('nivel', ''))
        prefijo = request.POST.get('prefijo', '').upper()
        # obtenemos el objeto curso atravez de la clave primaria para poder hacer una relacion Many-to-one
        # ? Documentacion: https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/
        course = Course.objects.get(pk=nivel)

        # se confirma que existe la asignatura y se guarda 
        subject = Subjects.objects.get(pk=subject_id)
        subject.subject = asignatura
        subject.course = course
        subject.prefix = prefijo
        subject.save()
        return JsonResponse({'message': 'Asignatura editada exitosamente'})
    
@login_required(login_url="/login/")
def delete_subjects(request):
    if request.method == 'POST':
        subject_id = request.POST.get('id', '')
        subject = Subjects.objects.get(pk=subject_id)
        subject.delete()
        return JsonResponse({'message': 'Asignatura eliminada exitosamente'})
    else:
        return JsonResponse({'message': 'error'})
    


# peticion de docentes para campo select2
@login_required(login_url="/login/")
def get_profesors(request):
    profesors = user_info.objects.filter(departament='docente').values()
    return JsonResponse({'data': list(profesors)})


# crud Assignaments
@login_required(login_url="/login/")
def get_assignments(request):
    assignments = Assignments.objects.values('id', 'teacher__user__username', 'teacher__user__user_info__first_name',
                     'teacher__user__user_info__last_name', 'teacher__user__user_info__id', 'subject__subject', 'subject__id')
    return JsonResponse({'data': list(assignments)})

@login_required(login_url="/login/")
def add_assignment(request):
    if request.method == 'POST':
        teacher = request.POST.get('docente', '')
        subject = request.POST.get('asignatura', '')
        teacher_obj = user_info.objects.get(pk=teacher)
        subject_obj = Subjects.objects.get(pk=subject)
        new_assignment = Assignments(teacher=teacher_obj, subject=subject_obj)
        new_assignment.save()
        return JsonResponse({'message': 'Asignacion agregada exitosamente'})
    else:
        return JsonResponse({'message': 'error'})
    
@login_required(login_url="/login/")
def edit_assignment(request):
    if request.method == 'POST':
        assignment_id = request.POST.get('id', '')
        teacher = request.POST.get('docente', '')
        subject = request.POST.get('asignatura', '')

        print(assignment_id, teacher, subject)
        teacher_obj = user_info.objects.get(pk=teacher)
        subject_obj = Subjects.objects.get(pk=subject)
        assignment = Assignments.objects.get(pk=assignment_id)
        assignment.teacher = teacher_obj
        assignment.subject = subject_obj
        assignment.save()
        return JsonResponse({'message': 'Asignacion editada exitosamente'})
    else:
        return JsonResponse({'message': 'error'})
    
@login_required(login_url="/login/")
def delete_assignment(request):
    if request.method == 'POST':
        assignment_id = request.POST.get('id', '')
        assignment = Assignments.objects.get(pk=assignment_id)
        assignment.delete()
        return JsonResponse({'message': 'Asignacion eliminada exitosamente'})
    else:
        return JsonResponse({'message': 'error'})