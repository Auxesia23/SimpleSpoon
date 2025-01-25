from django.shortcuts import render

def handler400(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def handler401(request, exception=None):
    return render(request, 'errors/401.html', status=401)

def handler403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def handler404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def handler405(request, exception=None):
    return render(request, 'errors/405.html', status=405)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

def handler502(request):
    return render(request, 'errors/502.html', status=502)

def handler503(request):
    return render(request, 'errors/503.html', status=503)
