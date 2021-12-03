import urllib.request, json


def load_json_from_url(url):
    with urllib.request.urlopen(url) as url_data:
        data = json.loads(url_data.read().decode())
    return data
