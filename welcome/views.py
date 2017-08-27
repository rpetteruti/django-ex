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
        os.chdir("/opt/app-root/src/")
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print (filename)
        os.system("rm -rf frames/*")
        #os.system("mkdir frames")
        os.system("unzip "+filename+ " -d frames/")
        os.system("rm "+filename)
        os.chdir("/darknet/darknet-master/")
        #os.system("/darknet/darknet-master/darknet detect /darknet/darknet-master/cfg/yolo.cfg /darknet/darknet-master/yolo.weights /opt/app-root/src/"+filename)
        #output_command = os.popen("/darknet/darknet-master/darknet detect /darknet/darknet-master/cfg/yolo.cfg /darknet/darknet-master/yolo.weights /opt/app-root/src/frames/"+filename).read()
        output_command = os.popen("python examples/folderDetector.py /opt/app-root/src/frames/").read()
        #os.system("python examples/folderDetector.py /opt/app-root/src/frames/")


        print("Command: "+output_command)
        uploaded_file_url = fs.url(filename)
        return render(request, 'welcome/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'output_command': output_command
        })
    return render(request, 'welcome/simple_upload.html')
