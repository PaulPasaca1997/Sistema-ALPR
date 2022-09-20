from ast import Div
from gzip import READ
from http.client import HTTPResponse, responses
from re import template
from urllib import response
from django.shortcuts import render, redirect
from torch import instance_norm
from django.contrib import auth
# Create your views here.
import numpy as np
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from administracion import utils
from administracion.deeplearning import OCR, VideoCamera
from administracion.forms import PlacaForm, UsuarioForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from django.views.generic import View
import pytesseract
#from administracion.deeplearning import OCR
from django.http import StreamingHttpResponse

import os
import cv2
from administracion.models import Placa

from administracion.utils import render_to_pdf



pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(
    BASE_PATH, 'D:/ALPR/administracion/static/upload')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
archivo_video = None
grabando = False
FRAMES_VIDEO = 20.0
RESOLUCION_VIDEO = (640, 480)


def principal(request):

    return render(request, "principal.html")


def index(request):

    return render(request, 'camara.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request): 
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
    ret, frame = cap.read()
    cv2.imwrite('D:/ALPR/administracion/static/upload/prueba.jpg', frame)
    cap.release()
    return render(request, 'index.html', {'dircamara':'D:/ALPR/administracion/static/upload/prueba.jpg'})



"""
def webcam_feed(request):
    return StreamingHttpResponse(gen(IPWebCam()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
"""

class reporte(View):
    def get(self, request, *args, **kwargs):
        template_name = "reportes.html"
        placa = Placa.objects.all()
        data = {
            'placa': placa
        }
        pdf = render_to_pdf(template_name, data)
        return HttpResponse(pdf, content_type='application/pdf')



def ocr(request):

    if request.method == 'POST':
        upload_file = request.FILES['image_name'] 
        print("upload file 93", upload_file)
        fs = FileSystemStorage()
        filename = fs.save(upload_file.name, upload_file)
        print("upload file 96" ,filename)

        uploaded_file_url = fs.url(filename)
        print("upload file 99", uploaded_file_url)

        #filename = upload_file.filename
        #path_save = os.path.join(UPLOAD_PATH, filename)
        #upload_file.save(path_save)
        text = OCR(filename, uploaded_file_url)
                
        print("LEE AQUI EL RQS", text)


        return render(request, 'index.html', {'upload_image':upload_file, 'text':text,'upload':True})


    return render(request, "index.html")

"""
def fotos(request):
    if request.method == 'POST' :
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'index.html')

"""

def administracion(request):
    return render(request, "administracion.html")


def registroUsuario(request):

    if request.user.is_authenticated:
        return redirect('administracion')
    else:
        form = UsuarioForm()
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                form.save()

                return redirect('listar')

        context = {'form': form}
        return render(request, 'registro.html', context)

def editar(request, note_id):
    usuario = User.objects.get(id = note_id)
    form = UsuarioForm(instance = usuario)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar')
        
    context = {'form':form}
    return render(request, 'registro.html', context)


def listarUsuario(request):
    context = {'lista': User.objects.all()}
    return render(request, "lista.html", context)



def eliminar(request, note_id):
    usuario = User.objects.get(id = note_id)
    usuario.delete()
    return redirect('principal')

def registroPlaca(request):

    if request.user.is_authenticated:
        return redirect('administracion')
    else:
        form = PlacaForm()
        if request.method == 'POST':
            form = PlacaForm(request.POST)
            if form.is_valid():
                form.save()
                placa = form.cleaned_data.get('placa')
                messages.success(request, 'PLACA REGISTRADA!' + placa)

                return redirect('administracion')

        context = {'form': form}
        return render(request, 'registroPlaca.html', context)


def loginAdm(request):
    if request.user.is_authenticated:
        return redirect('administracion')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('administracion')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'loginA.html', context)


def loginPageU(request):
    if request.user.is_authenticated:
        return redirect('principal')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('principal')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'loginU.html', context)


def logoutUser(request):
    logout(request)
    return redirect('principal')





