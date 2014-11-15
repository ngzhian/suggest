from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def suggest(request):
    content = request.GET.get('content')
    current_word = request.GET.get('current')
    if not content:
        return JsonResponse(dict(err='no content'))
    result = _suggest(current_word, content)
    return JsonResponse(dict(result=result))


def _suggest(current_word, content):
    return ['asdf', 'bcd']
