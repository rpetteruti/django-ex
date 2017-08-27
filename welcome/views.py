import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from . import database
from .models import PageView

# Create your views here.

def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)


    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    return HttpResponse(PageView.objects.count())

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print (filename)
        os.chdir("/darknet/darknet-master/")
        os.system("/darknet/darknet-master/darknet detect /darknet/darknet-master/cfg/tiny-yolo.cfg /darknet/darknet-master/tiny-yolo.weights /opt/app-root/src/"+filename)
        uploaded_file_url = fs.url(filename)
        return render(request, 'welcome/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'welcome/simple_upload.html')
