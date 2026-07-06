from django.http import JsonResponse


def hello(request):
    return JsonResponse({'message': 'Hello from Django + Jenkins i love you'})

def health(request):
    return JsonResponse({'status': 'ok'})
