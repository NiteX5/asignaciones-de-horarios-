# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('delete_course/<int:id>', views.delete_course, name='delete_course'),
    
    # ajax users
    path('get_users/', views.get_users, name='get_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('delete_user/', views.delete_user, name='delete_user'),

    #ajax subjects
    path('get_subjects/', views.get_subjects, name='get_subjects'),
    path('add_subject/', views.add_subjects, name='add_subject'),
    path('edit_subjects/', views.edit_subjects, name='edit_subjects'),
    path('delete_subjects/', views.delete_subjects, name='delete_subjects'),

    # ajax docents
    path('get_docents/', views.get_profesors, name='get_docents'),

    # ajax courses
    path('get_courses/', views.get_courses, name='get_courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('edit_course/', views.edit_course, name='edit_course'),
    path('delete_course/', views.delete_course, name='delete_course'),

    # ajax Assignments
    path('get_assignments/', views.get_assignments, name='get_assignments'),
    path('add_assignment/', views.add_assignment, name='add_assignment'),
    path('edit_assignment/', views.edit_assignment, name='edit_assignment'),
    path('delete_assignment/', views.delete_assignment, name='delete_assignment'),

    # ajax Schedule
    path('get_subjects_assignament/<int:id>', views.get_subjects_assignament, name='get_subjects_assignament'),
    path('get_courses/<int:id>', views.get_course_byId, name='get_course_id'),
    path('save_schedule/', views.save_schedule, name='save_schedule'),
   # Tambien ocupado en listCalerdar 
    path('get_events/<int:id>', views.get_events, name='get_events'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('update_event/', views.update_event, name='update_event'),

    # ajax listCalendar
    path('get_course_listCalendar/<int:id>', views.get_course_listCalendar, name='get_course_listCalendar'),


    # ajax settings
        #Tambien ocupado por la vista de horario docentes
    path('get_settings/', views.get_current_user_info, name='get_settings'),
    path('update_settings/', views.update_settings, name='update_settings'),



    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
