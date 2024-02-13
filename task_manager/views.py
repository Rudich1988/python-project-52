from django.shortcuts import render
from task_manager.settings import SECRET_KEY


def index(request):
    return render(request, 'index.html', context={'message': SECRET_KEY})