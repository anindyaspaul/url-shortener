from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required

from .forms import UrlSubmissionForm
from .utils import add_url_redirection, get_redirection_keys, get_target_url


@login_required
def index(request: HttpRequest, slug: str = None):
    target_url = get_target_url(slug)
    if target_url is not None:
        return redirect(to=target_url)

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
