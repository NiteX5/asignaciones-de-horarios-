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

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
