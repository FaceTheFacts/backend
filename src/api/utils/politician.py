import urllib.request
from urllib.error import HTTPError
from typing import List

from src.db import models


def add_image_urls_to_politicians(politicians: List[models.Politician]):
    for politician in politicians:
        image_url = f"https://candidate-images.s3.eu-central-1.amazonaws.com/{politician.id}.jpg"

        try:
            urllib.request.urlopen(image_url)
            politician.__dict__["image_url"] = image_url
        except HTTPError:
            politician.__dict__["image_url"] = None

    return politicians
