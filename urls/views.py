from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import UrlSubmissionForm
from .utils import add_url_redirection, get_redirection_keys, get_target_url


@login_required
def index(request: HttpRequest):
    url_submission_form = UrlSubmissionForm()

    if request.method == 'POST':
        url_submission_form = UrlSubmissionForm(request.POST)
        if url_submission_form.is_valid():
            add_url_redirection(request.user, **url_submission_form.cleaned_data)

    context = {
        'url_submission_form': url_submission_form,
        'redirection_keys': get_redirection_keys(request.user)
    }
    return render(request, 'index.html', context=context)


def visit(request: HttpRequest, slug: str = None):
    target_url = get_target_url(slug)
    if target_url is None:
        target_url = '/'
    return redirect(to=target_url)


def signup(request: HttpRequest):
    user_creation_form = UserCreationForm()

    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            username = user_creation_form.cleaned_data['username']
            password = user_creation_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

    if request.user.is_authenticated:
        return redirect(to='/')

    context = {
        'user_creation_form': user_creation_form
    }
    return render(request, 'signup.html', context=context)
