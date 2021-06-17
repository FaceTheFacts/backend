import json

from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    data = {"msg": "Hello, world."}
    return HttpResponse(json.dumps(data), content_type="application/json")
