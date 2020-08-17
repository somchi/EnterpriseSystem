from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str
from json import dumps

def filter(request, model_class, field_name):
    try:
        kwargs = {smart_str(field_name): request.GET['q']}
    except KeyError:
        raise Http404
    qs = model_class.objects.filter(**kwargs).values('pk', 'name')
    response = HttpResponse(
        content=dumps(list(qs)),
        mimetype='application/json'
    )
    return response
