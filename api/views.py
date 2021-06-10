import json

from django.http import HttpResponse


def index(request):
    data = {"msg": "Hello, world."}
    return HttpResponse(json.dumps(data), content_type="application/json")
