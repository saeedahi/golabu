import math
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
from django.utils.text import slugify


def calculate_reading_time(html):
    text = strip_tags(html)
    words = len(text.split())

    return max(1, math.ceil(words / 200))

def add_heading_ids(html):
    soup = BeautifulSoup(html, 'html.parser')

    for heading in soup.find_all(['h2', 'h3', 'h4']):
        if not heading.get("id"):
            heading['id'] = slugify(heading.text, allow_unicode=True)

    return str(soup)

def generate_toc(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    toc = []

    for heading in soup.find_all(
        ["h2", "h3"]
    ):

        toc.append({
            "title": heading.text,
            "id": heading.get("id"),
            "level": heading.name
        })

    return toc