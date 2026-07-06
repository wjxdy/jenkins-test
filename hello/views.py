from django.http import JsonResponse


def hello(request):
    return JsonResponse({'message': 'Hello from Django + Jenkins'})


def health(request):
    return JsonResponse({'status': 'ok'})
