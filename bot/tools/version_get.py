import requests

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from bot.config import REPO_URL
from bot.tools.string_escape import string_escape


def version_get():
    try:
        resp = requests.get(REPO_URL, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        span_class = 'css-truncate css-truncate-target text-bold mr-2'
        elm = soup.find('span', class_=span_class)
        version = string_escape(elm.text, '.')
    except (Exception, RequestException):
        return None
    return version
