import os

import requests


def generate_authenticated_header():
    def authenticate():
        resp = requests.post(
            os.environ["POLITRACK_API_URL"] + "/auth",
            json={
                "username": os.environ["POLITRACK_USERNAME"],
                "password": os.environ["POLITRACK_SECRET_PASSWORD"],
            },
        )
        if resp.status_code == 200:
            return resp.json()["access_token"]
        print(resp.status, resp.text)
        return None

    token = authenticate()
    if token is None:
        raise RuntimeError("Could not authenticate")
    return {"Authorization": "Bearer " + token}
