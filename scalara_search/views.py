from django.shortcuts import render, HttpResponseRedirect, redirect
import boto3
from .forms import SearchForm
from boto3.dynamodb.conditions import Key
from botocore.client import Config
import os


# Create your views here.
def search_files(request):
    if not request.session.get('user', None):
        return redirect('login')
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', aws_access_key_id=os.environ['access_key_id'],
         aws_secret_access_key= os.environ['access_key_secret'])
    table = dynamodb.Table('upload_metadata')
    if request.method == "POST":
        response = None
        form = SearchForm(request.POST)
        if form.is_valid():
            for key in form.cleaned_data.keys():
                if form.cleaned_data[key]:
                    key_value = form.cleaned_data[key]
                    if key == 'name':
                        response = table.query(
                            KeyConditionExpression=(Key('benutzer').eq(request.session['user']) & Key(key).eq(key_value))
                        )
                    else: 
                        response = table.query(
                            IndexName=f'{key}-index',
                            KeyConditionExpression=(Key('benutzer').eq(request.session['user']) & Key(key).eq(key_value))
                        )
                    print(response)
                    break
        if not response:
            response = table.query(
                                KeyConditionExpression=(Key('benutzer').eq(request.session['user']))
                        )
    else:
        response = table.query(
                                KeyConditionExpression=(Key('benutzer').eq(request.session['user']))
                            )
    data = response['Items']
    print(data)
    form = SearchForm()
    return render(request, "search.html",{"form": form, "metadataItems": data, "username": request.session['user']})


def download_files(request, file_key):
    s3 = boto3.resource(
        "s3", 
        region_name='eu-central-1', 
        config=Config(signature_version="s3v4"),
        aws_access_key_id=os.environ['access_key_id'],
        aws_secret_access_key= os.environ['access_key_secret'],
    )

    url = s3.meta.client.generate_presigned_url(
        "get_object", 
        Params={"Bucket": 'aufgabe-hady', "Key": file_key, 'ResponseContentDisposition': 'attachment'}, 
        ExpiresIn='120',
    )
    # return HttpResponse(file_key) 
    return HttpResponseRedirect(url)