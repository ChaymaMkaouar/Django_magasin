from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('jeu/index.html')
    return HttpResponse(template.render(request=request))

def aurevoir(request):
    template = loader.get_template('jeu/aurevoir.html')
    return HttpResponse(template.render(request=request))

