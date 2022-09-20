
from re import template
from django.urls import path, include
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from administracion import views


urlpatterns = [
    path('', views.principal, name='principal'),
    
    path('inicio/', views.principal, name='inicio'),

    path('camara/', views.index, name='principal'),

    #path('ocr/', views.ocr, name='ocr'),

    # path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('administracion/', views.administracion, name='administracion'),

    path('registrar/', views.registroUsuario, name="registrar"),
    path('listar/', views.listarUsuario, name="listar"),

    path('eliminar/<note_id>/', views.eliminar, name="eliminar"),
    path('editar/<note_id>/', views.editar, name="editar"),

    path('loginadm/', views.loginAdm, name="loginadm"),
    path('loginusu/', views.loginPageU, name="loginusu"),
    path('logout/', views.logoutUser, name="logout"),
    path('registroplaca/', views.registroPlaca, name="registroplaca"),
    path('reporte/', views.reporte.as_view(), name="reporte"),
    #path('camara/', views.cambase, name='camara'),
    #path('camara/video_feed/', views.video_feed, name='vide'),
    path('video_feed', views.video_feed, name='video_feed'),
    #path('webcam_feed', views.webcam_feed, name='webcam_feed'),


    path('ocr/', views.ocr, name="ocr"),

    #path('usuario', views.usuario, name='usuario'),
    #path('<int:id>/', views.usuario, name='usuario_edit'),
    #path('lista/', views.lista, name='lista'),
    #path('eliminar/<int:id>/', views.eliminar, name='usuario_delete'),
    #path('listaplaca/', views.listaPlaca, name='listaPlaca'),




]
