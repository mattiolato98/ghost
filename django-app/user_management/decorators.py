from django.http import HttpResponseNotFound
from django.shortcuts import redirect


def not_authenticated_only(func):
    def check_and_call(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('transcribe:transcription-list')
        return func(request, *args, **kwargs)
    return check_and_call


def manager_required(func):
    def check_and_call(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_manager:
            return func(request, *args, **kwargs)
        return HttpResponseNotFound()
    return check_and_call
