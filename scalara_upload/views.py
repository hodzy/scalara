from django.shortcuts import render, redirect
from .forms import UploadFileForm
import boto3
from django.core.files.storage import default_storage
import random
import string


# Create your views here.

def s3_upload(file_metadata, file):
    s3 = boto3.client('s3')
    metadata={
        "Metadata": {
            "name": file_metadata['name'],
            "ersteller": file_metadata['ersteller'],
            "benutzer": file_metadata['benutzer'],
            "other": file_metadata['other'],
        }
    }

    s3.upload_file(file, 'aufgabe-hady', file_metadata['name'], ExtraArgs=metadata)

def upload_files(request):
    print('user is: ', request.user.is_authenticated)
    if not request.session.get('user', None):
        return redirect('login')
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # print('post')
        # print(request.FILES)
        # print(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            uploaded_file = form.cleaned_data['file']
            del form.cleaned_data['file']
            metadata = {"Metadata": form.cleaned_data  }

            random_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
            metadata['Metadata']['file_key'] = random_name
            metadata['Metadata']['benutzer'] = request.session['user']
            print(metadata)
            default_storage.object_parameters.update(metadata)
            default_storage.save(random_name, uploaded_file)

    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form, "username": request.session['user']})