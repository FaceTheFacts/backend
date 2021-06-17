import json
import requests

from django.http import HttpRequest, HttpResponse

from .preprocessors import preprocess_occupation, preprocess_party


BASE_URL = "https://abgeordnetenwatch.de/api/v2"


def index(request: HttpRequest) -> HttpResponse:
    data = {"msg": "Hello, world."}
    return HttpResponse(json.dumps(data), content_type="application/json")


def politicians(request: HttpRequest, id: int) -> HttpResponse:
    # fetch data
    data = requests.get(f"{BASE_URL}/politicians/{id}").json()["data"]

    # preprocess attributes
    data["occupation"] = preprocess_occupation(data["occupation"])
    data["party"]["label"] = preprocess_party(data["party"]["label"])

    # return json
    return json_response(data)


def json_response(data: dict) -> HttpResponse:
    return HttpResponse(json.dumps(data), content_type="application/json")
