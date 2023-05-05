from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.forms import SetPasswordForm
from core.models import User
import os

def reset_password(request):
    try:
        server_host = os.environ.get('SERVER_HOST')
        token = request.GET.get('token')
        uidb64 = request.GET.get('uidb64')
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'reset_pass.html', {'server_host': server_host})
        else:
            return render(request, 'invalid.html')
    except Exception as e:
        print("error : ", e.args[0])
        user = None