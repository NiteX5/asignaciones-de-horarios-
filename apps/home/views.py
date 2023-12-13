from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import *
from datetime import timedelta, datetime
from django.core.serializers import serialize
import json


@login_required(login_url="/login/")
def index(request):
    context = {}
    current_user = User.objects.get(username=request.user)
    user_info_instance = user_info.objects.get(user=current_user)
    context = {'departament': user_info_instance.departament, 'segment': 'index', 'id': user_info_instance.id}
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
        context = {'departament': user_info_instance.departament, 'segment': 'index', 'form': 'form', 'id': user_info_instance.id}

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
        teaching = request.POST.get('teaching', '')

        
        # Verifica si el curso ya existe
        exist = Course.objects.filter(course=course_name, education = teaching).exists()
        if exist:
            return JsonResponse({'message': 'Curso ya existe'}, status = 400)

        new_course = Course(course=course_name, education=teaching)
        new_course.save()
        return JsonResponse({'message': 'Curso agregado exitosamente'})
    else:
        return JsonResponse({'message': 'error del sistema'})

@login_required(login_url="/login/")
def edit_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('id', '')
        course_name = request.POST.get('course', '').upper()
        course_education = request.POST.get('teaching', '')
        course = Course.objects.get(pk=course_id)
        course.course = course_name
        course.education = course_education
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
            return JsonResponse({'message': 'Usuario '+ username + ' ya existe'}, status = 400)
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
        return JsonResponse({'message': 'error'}, status = 400)
    
    
@login_required(login_url="/login/")
@require_POST
def delete_user(request):
    user_id = request.POST.get('id', '')
    uid = user_info.objects.filter(pk=user_id).values('user_id')
    #user_infos = user_info.objects.get(pk=user_id)
    #user_infos.delete()
    print(uid[0]['user_id'])
    user = User.objects.get(pk=uid[0]['user_id'])
    user.delete()

        
    return JsonResponse({'message': 'Usuario eliminado exitosamente'})
    
# crud asignaturas

@login_required(login_url="/login/")
def get_subjects(request):
    subjects = Subjects.objects.values('id', 'subject','education' , 'prefix')
    return JsonResponse({'data': list(subjects)})

@login_required(login_url="/login/")
def add_subjects(request):
    if request.method == 'POST':
        asignatura = request.POST.get('asignatura', '')
        Enseñanza = request.POST.get('teaching', '')
        prefijo = request.POST.get('prefijo', '').upper()
        
        # obtenemos el objeto curso atravez de la clave primaria para poder hacer una relacion Many-to-one
        # ? Documentacion: https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/
        
        # Verifica si la asignatura ya existe
        exist = Subjects.objects.filter(subject=asignatura, education=Enseñanza).exists()
        if exist:
            return JsonResponse({'message': 'Asignatura ya existe'}, status = 400)
        else:
            new_subject = Subjects(subject=asignatura, prefix=prefijo, education=Enseñanza)
            new_subject.save()
            return JsonResponse({'message': 'Asignatura agregada exitosamente'})
    else:
        return JsonResponse({'message': 'error'}, status = 400)

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
        return JsonResponse({'message': 'error'}, status = 400)
    


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

        assignament = Assignments.objects.filter(teacher=teacher_obj, subject=subject_obj).exists()
        if assignament:
            return JsonResponse({'message': 'Asignacion ya existe'}, status = 400)

        new_assignment = Assignments(teacher=teacher_obj, subject=subject_obj)
        new_assignment.save()
        return JsonResponse({'message': 'Asignacion agregada exitosamente'})
    else:
        return JsonResponse({'message': 'error'}, status = 400)
    
@login_required(login_url="/login/")
def edit_assignment(request):
    if request.method == 'POST':
        assignment_id = request.POST.get('id', '')
        teacher = request.POST.get('docente', '')
        subject = request.POST.get('asignatura', '')
        teacher_obj = user_info.objects.get(pk=teacher)
        subject_obj = Subjects.objects.get(pk=subject)
        assignment = Assignments.objects.get(pk=assignment_id)
        assignment.teacher = teacher_obj
        assignment.subject = subject_obj
        assignment.save()
        return JsonResponse({'message': 'Asignacion editada exitosamente'})
    else:
        return JsonResponse({'message': 'error'}, status = 400)
    
@login_required(login_url="/login/")
def delete_assignment(request):
    if request.method == 'POST':
        assignment_id = request.POST.get('id', '')
        assignment = Assignments.objects.get(pk=assignment_id)
        assignment.delete()
        return JsonResponse({'message': 'Asignacion eliminada exitosamente'})
    else:
        return JsonResponse({'message': 'error'}, status = 400)
    

# crud horarios

@login_required(login_url="/login/")
def get_subjects_assignament(request, id):

    # Obtener las asignaturas asignadas a un profesor
    subjects = Assignments.objects.filter(teacher_id=id).values('subject__subject', 'subject__id', 'subject__education')
    print(id)
    
    # Obtener los cursos de las asignaturas
    course = Course.objects.values('id', 'course', 'education')
    # Crear un arreglo para almacenar los datos
    data = []
    # Recorrer las asignaturas
    for subject in subjects:
        # Recorrer los cursos
        for c in course:
            # Comprobar si el curso es igual a la asignatura
            print(subject['subject__education'])
            if subject['subject__education'].upper() == c['education'].upper() or subject['subject__education'].upper() == 'AMBAS':
                if c not in data:
                    data.append({'course': c['course'], 'course_id': c['id'], 'subject': subject['subject__subject'], 'subject_id': subject['subject__id']})
    return JsonResponse({'data': list(data)})

def get_course_byId(request, id):
    # Obtener las asignaturas asignadas a un profesor
    subjects = Assignments.objects.filter(teacher=id).values('subject__education')
    # Obtener los cursos de las asignaturas
    courses = Course.objects.values('id', 'course', 'education')

    data = []
    for subject in subjects:
        for course in courses:
            if subject['subject__education'] == course['education'] or subject['subject__education'].upper() == 'AMBAS':
                if course not in data:
                    data.append({'id': course['id'], 'course': course['course'], 'education': course['education']})
                
    return JsonResponse({'data': data})

def get_subjects_by_teacher(request, teacher_id):
    # Obtener las asignaturas asignadas a un profesor
    assignments = Assignments.objects.filter(teacher_id=teacher_id)
    subjects = [assignment.subject for assignment in assignments]

    # Serializar los datos y devolverlos como JSON
    data = [{'id': subject.id, 'subject': subject.subject, 'course': subject.course.course} for subject in subjects]
    return JsonResponse({'data': data})

@csrf_exempt
@require_POST
def save_schedule(request):
    # Obtener datos del cuerpo de la solicitud POST
    day = request.POST.get('day', '')
    hour = request.POST.get('start','')
    column = request.POST.get('column','')
    subject_id = request.POST.get('subjectId','')
    teacher_id = request.POST.get('teacherId','')
    course_id = request.POST.get('courseId', '')
    title = request.POST.get('title', '') 
    # verificar que no tenga horario en ese dia y hora
    schedule = Schedule.objects.filter(day_of_week=column, start=hour, course = course_id).exists()
    if schedule:
        return JsonResponse({'message': 'Ya existe un horario en ese dia y hora (No guardado elimine el objeto arrastrado)'}, status = 400)
    else:
        # Obtener los objetos de la base de datos
        subject = Subjects.objects.get(pk=subject_id)
        teacher = user_info.objects.get(pk=teacher_id)
        course = Course.objects.get(pk=course_id)
        # Crear el objeto Schedule
        schedule = Schedule(title= title ,start=hour, subject=subject, teacher=teacher, course=course, day_of_week=column, end='00:45:00')
        schedule.save()
        return JsonResponse({'message': 'Horario guardado exitosamente'})


@login_required(login_url="/login/")
def get_events(request, id):
    # Obtener todos los horarios
    schedules = Schedule.objects.filter(teacher=id)
    # Serializar los datos y devolverlos como JSON
    data = []
    for schedule in schedules:
       
        idSc = schedule.id
        
        duration = schedule.end.strftime('%H:%M')  # Asegúrate de que esto es una duración válida

        # Convertir la duración a timedelta
        duration_parts = duration.split(":")
        duration_timedelta = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]))


        # Convertir la cadena de fecha de inicio a un objeto datetime
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        start = today_str + 'T' + str(schedule.start)[11:19]
        
        # Calcular la fecha de finalización
        end = (datetime.strptime(start, "%Y-%m-%dT%H:%M:%S") + duration_timedelta).strftime("%Y-%m-%dT%H:%M:%S")


        title = schedule.title
        resource = schedule.day_of_week
        extendedProps = {'course': schedule.course.id, 'subject': schedule.subject.id, 'teacher': schedule.teacher.id}
        data.append({'id': idSc, 'title': title, 'start': start, 'end': end, 'resourceId': resource, 'extendedProps': extendedProps, 'allDay': False})

    print(data)

    return JsonResponse(data, safe=False)  # Devolver la matriz directamente

@login_required(login_url="/login/")
@require_POST
@csrf_exempt
def delete_event(request):
    event_id = request.POST.get('id', '')
    event = Schedule.objects.get(pk=event_id)
    event.delete()
    return JsonResponse({'message': 'Horario eliminado exitosamente'})

@login_required(login_url="/login/")
@require_POST
@csrf_exempt
def update_event(request):
    try:
        event_id = request.POST.get('id', '')
        event = Schedule.objects.get(pk=event_id)
        event.title = request.POST.get('title', '')
        event.start = request.POST.get('start', '')
        event.end = request.POST.get('end', '')
        event.day_of_week = request.POST.get('column', '')
        teacher_id = request.POST.get('teacherId', '')
        course_id = request.POST.get('courseId', '')
        subject_id = request.POST.get('subjectId', '')
        print(teacher_id)
        print(course_id)
        print(subject_id)
        subject = Subjects.objects.get(pk=subject_id)
        teacher = user_info.objects.get(pk=teacher_id)
        course = Course.objects.get(pk=course_id)
        event.teacher = teacher
        event.course = course
        event.subject = subject
        event.save()
        return JsonResponse({'message': 'Horario editado exitosamente'})
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Refresque la pagina'}, status = 400)
    
#Schedule list view
@login_required(login_url="/login/")
def get_course_listCalendar(request, id):
    try:
        schedule = Schedule.objects.filter(course = id)
        print(schedule)
        data = []
        for schedule in schedule:
            id = schedule.id
            duration = schedule.end.strftime('%H:%M')
            duration_parts = duration.split(":")
            duration_timedelta = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]))
            today = datetime.now()
            today_str = today.strftime("%Y-%m-%d")
            start = today_str + 'T' + str(schedule.start)[11:19]
            end = (datetime.strptime(start, "%Y-%m-%dT%H:%M:%S") + duration_timedelta).strftime("%Y-%m-%dT%H:%M:%S")
            title = schedule.title
            resource = schedule.day_of_week
            extendedProps = {'course': schedule.course.id, 'subject': schedule.subject.id, 'teacher': schedule.teacher.id}
            data.append({'id': id, 'title': title, 'start': start, 'end': end, 'resourceId': resource, 'extendedProps': extendedProps, 'allDay': False})

        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Algo anda mal refresque porfavor'}, status = 400)
   

# Settings view
@login_required(login_url="/login/")
def get_current_user_info(request):
    current_user = User.objects.get(username=request.user)
    user_info_instance = user_info.objects.get(user=current_user)

    # Construye un diccionario con los campos relevantes
    user_info_data = {
        'id': user_info_instance.id,
        'first': user_info_instance.first_name,
        'last': user_info_instance.last_name,
        'phone': user_info_instance.phone_number,
        'email': user_info_instance.email,
        'departament': user_info_instance.departament,
    }
    
    return JsonResponse({'data': user_info_data}, safe=False)

@login_required(login_url="/login/")
@require_POST
def update_settings(request):
    user_id = request.POST.get('id', '')
    first_name = request.POST.get('first', '')
    last_name = request.POST.get('last', '')
    phone_number = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    user_info_obj = user_info.objects.get(id=user_id)
    user_info_obj.first_name = first_name.capitalize()
    user_info_obj.last_name = last_name.capitalize()
    user_info_obj.phone_number = phone_number
    user_info_obj.email = email
    user_info_obj.save()
    return JsonResponse({'message': 'Usuario editado exitosamente'})
