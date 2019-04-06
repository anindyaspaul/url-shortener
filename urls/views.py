from django.shortcuts import render
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required

from .forms import UrlSubmissionForm
from .utils import add_url_redirection, get_redirection_keys


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
