from django.urls import path
from . import views

urlpatterns = [

    # dashboard page
    path('', views.task_list, name='task_list'),

    # complete task
    path('complete/<int:id>/', views.complete_task, name='complete_task'),

    # delete task
    path('delete/<int:id>/', views.delete_task, name='delete_task'),

    #update
    path('update/<int:id>/', views.update_task, name='update_task'),

    #register
    path("register/", views.register, name="register"),

    #Login
    path("login/", views.user_login, name="user_login"),
]